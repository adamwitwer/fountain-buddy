"""Burst → best bird → crop → species guess → stored visit (no Discord here).

Frames are saved unmarked. Only the Discord preview has a box drawn on it, so photos stay
usable as training data (v1 drew into the originals).

Known not-a-bird spots: a box Adam answered "Not a bird" (the tray's bracket at dusk, the
camera cable) keeps scoring as a bird. A detection on such a spot is dropped unless the
classifier's first guess is a species, so a bird standing on the bracket still posts.
A swaying ivy sprig lands a little differently each time (IoU 0.2-0.9 between repeats),
so a spot matches at IoU 0.5. Matching on overlap with the smaller box would be looser
still, but it dropped a wren standing inside the bracket's box in replay.

Night: the camera switches to infrared after dark, and its frames are pure greyscale.
No birds visit then, but mice do (94 posts in one night, 2026-10-19). An infrared burst
posts only if the classifier's first guess is a species or Squirrel; the camera stays in
infrared past sunrise, and a wren came at 07:35 that way.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from fountain_buddy import db, species
from fountain_buddy.classifier import Classifier
from fountain_buddy.detect import Detection, Detector, iou

log = logging.getLogger(__name__)

PREVIEW_WIDTH = 1600
REJECTS_KEPT_DAYS = 7
SPOT_IOU = 0.5  # the bracket repeats at ~0.95, the ivy sprig at 0.5-0.9
SPOT_DAYS = 30
POSTABLE = {*species.SPECIES, species.SQUIRREL}
INFRARED_SATURATION = 2  # mean HSV saturation: infrared frames are 0, daylight 38-70


@dataclass(frozen=True)
class Sighting:
    visit_id: int
    taken_at: dt.datetime
    ranked: list[tuple[str, float]]  # every label, most likely first
    det_conf: float
    preview_path: Path


def not_bird_spots(store: Path, camera: str, now: dt.datetime) -> list[tuple[int, ...]]:
    """Boxes of this camera's visits answered "Not a bird" in the last SPOT_DAYS."""
    since = (now - dt.timedelta(days=SPOT_DAYS)).isoformat(timespec="seconds")
    with closing(db.connect(store)) as conn:
        rows = conn.execute(
            "SELECT c.x1, c.y1, c.x2, c.y2 FROM crops c JOIN visits v ON v.id = c.visit_id "
            "JOIN current_labels l ON l.visit_id = v.id "
            "WHERE v.source = 'live' AND v.camera = ? AND l.label = ? AND v.taken_at >= ?",
            (camera, species.NOT_A_BIRD, since),
        ).fetchall()
    return [tuple(r) for r in rows]


def best_detection(frames: list[np.ndarray], detector: Detector, spots=()):
    """(frame index, detection, on a known spot) for the best bird in the burst, or None.
    Anything off the known not-a-bird spots beats anything on them; then confidence."""
    best = None
    for i, frame in enumerate(frames):
        for det in detector.birds(frame):
            box = (det.x1, det.y1, det.x2, det.y2)
            on_spot = any(iou(box, spot) >= SPOT_IOU for spot in spots)
            if best is None or (not on_spot, det.conf) > (not best[2], best[1].conf):
                best = (i, det, on_spot)
    return best


def infrared(frame: np.ndarray) -> bool:
    """True for the camera's night (infrared) mode, whose frames have no colour."""
    small = cv2.resize(frame, (480, 270), interpolation=cv2.INTER_AREA)
    return cv2.cvtColor(small, cv2.COLOR_BGR2HSV)[..., 1].mean() < INFRARED_SATURATION


def preview(frame: np.ndarray, det: Detection) -> np.ndarray:
    scale = PREVIEW_WIDTH / frame.shape[1]
    small = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    p1 = (int(det.x1 * scale), int(det.y1 * scale))
    p2 = (int(det.x2 * scale), int(det.y2 * scale))
    cv2.rectangle(small, p1, p2, (80, 220, 255), 2)
    return small


class Pipeline:
    def __init__(self, store: Path, data_dir: Path, detector: Detector, classifier: Classifier,
                 camera: str = "tray", source: str = "live"):  # fmt: skip
        self.store, self.data_dir = store, data_dir
        self.detector, self.classifier, self.camera = detector, classifier, camera
        self.source = source  # 'test' for post-test: never trained on, never summarized
        db.init(store)

    def _save(self, rel: str, image: np.ndarray, quality: int = 92) -> None:
        path = self.data_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(path), image, [cv2.IMWRITE_JPEG_QUALITY, quality])

    def process(self, frames: list[np.ndarray], now: dt.datetime | None = None) -> Sighting | None:
        now = now or dt.datetime.now()
        stamp = now.strftime("%Y-%m-%d/%H%M%S")
        spots = not_bird_spots(self.store, self.camera, now)
        found = best_detection(frames, self.detector, spots)
        if found is None:
            # Keep one frame per empty burst for a week: detector misses show up here.
            self._save(f"rejects/{stamp}.jpg", frames[len(frames) // 2], quality=85)
            log.info("burst: no bird in %d frames", len(frames))
            return None
        idx, det, on_spot = found
        frame = frames[idx]
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = max(det.x1, 0), max(det.y1, 0), min(det.x2, w), min(det.y2, h)
        crop = frame[y1:y2, x1:x2]
        ranked = self.classifier.predict(crop)
        if ranked[0][0] not in POSTABLE:
            why = "spot" if on_spot else "night" if infrared(frame) else None
            if why:
                self._save(f"rejects/{stamp}-{why}.jpg", preview(frame, det), quality=85)
                log.info("burst: %s, not a bird (%s %.0f%%, bird %.2f)",
                         "known not-a-bird spot" if on_spot else "infrared",
                         ranked[0][0], 100 * ranked[0][1], det.conf)  # fmt: skip
                return None

        frame_rel = f"images/{self.camera}/{stamp}.jpg"
        self._save(frame_rel, frame, quality=95)
        with closing(db.connect(self.store)) as conn:
            visit_id = conn.execute(
                "INSERT INTO visits (taken_at, camera, image_path, source) VALUES (?, ?, ?, ?)",
                (now.isoformat(timespec="seconds"), self.camera, frame_rel, self.source),
            ).lastrowid
            crop_rel = f"crops/live/{visit_id}.jpg"
            self._save(crop_rel, crop, quality=95)
            conn.execute(
                "INSERT INTO crops (visit_id, method, x1, y1, x2, y2, det_conf, path) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (visit_id, self.detector.name, x1, y1, x2, y2, det.conf, crop_rel),
            )
            conn.execute(
                "INSERT INTO predictions (visit_id, model, label, confidence, top_k, predicted_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (visit_id, self.classifier.version, ranked[0][0], ranked[0][1],
                 json.dumps([[label, round(p, 4)] for label, p in ranked[:5]]),
                 now.isoformat(timespec="seconds")),
            )  # fmt: skip
            conn.commit()
        preview_rel = f"previews/{visit_id}.jpg"
        self._save(preview_rel, preview(frame, det), quality=88)
        log.info(
            "visit %d: %s %.0f%% (bird %.2f)", visit_id, ranked[0][0], 100 * ranked[0][1], det.conf
        )
        return Sighting(visit_id, now, ranked, det.conf, self.data_dir / preview_rel)

    def prune_rejects(self, today: dt.date | None = None) -> None:
        cutoff = (today or dt.date.today()) - dt.timedelta(days=REJECTS_KEPT_DAYS)
        for day in (self.data_dir / "rejects").glob("*"):
            try:
                if dt.date.fromisoformat(day.name) < cutoff:
                    for f in day.iterdir():
                        f.unlink()
                    day.rmdir()
            except ValueError:
                continue
