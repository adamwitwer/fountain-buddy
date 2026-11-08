"""Burst → best bird → crop → species guess → stored visit (no Discord here).

Frames are saved unmarked. Only the Discord preview has a box drawn on it, so photos stay
usable as training data (v1 drew into the originals).

Known not-a-bird spots: a box Adam answered "Not a bird" (the tray's bracket at dusk, the
camera cable) keeps scoring as a bird. A detection on such a spot is dropped unless the
classifier's first guess is a species, so a bird standing on the bracket still posts.
Spots are positions in the frame, so they reset when the camera moves (`camera_moves`).
A swaying ivy sprig lands a little differently each time (IoU 0.2-0.9 between repeats),
so a spot matches at IoU 0.5. Matching on overlap with the smaller box would be looser
still, but it dropped a wren standing inside the bracket's box in replay.

Night: the camera switches to infrared after dark, and its frames are pure greyscale.
No birds visit then, but mice do (94 posts in one night, 2026-10-19). An infrared burst
posts only if the classifier's first guess is a species or Squirrel; the camera stays in
infrared past sunrise, and a wren came at 07:35 that way.

Repeats: a bird at the tray trips motion every few seconds, and one titmouse made 22
posts in an hour. A burst whose first guess was posted in the last REPEAT_WINDOW isn't
posted again. A different guess still posts, since several species share the tray: a
flat 5-minute cooldown would have hidden 283 posts whose answer differed from the one
before (2026-10-23 to 29), this hides none that weren't mis-guessed.

Auto-accept: a guess of a species or Squirrel at AUTO_ACCEPT or above is posted as
accepted, with only a Change button. At 0.97 that was half the posts, and 6 of 600
answered ones were wrong (5 should have been Skip, 1 the wrong species). It is not a
label (see db.auto_accepts). SPOT_CHECK_SHARE of them ask anyway, to keep measuring.

Detector region: YOLO sees the 4K frame shrunk to 1280 px, a third of its size. With a
region set (`fountain-buddy crop`, saved in detector.json), it looks only at that part
of the frame, so birds there look bigger to it and nothing outside can fire. Crops, saved
frames and boxes stay in full-frame pixels. A region belongs to one view: once the camera
is recorded as moved after it was set, it stops applying until a new one is set.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import random
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
REPEAT_WINDOW = dt.timedelta(minutes=5)
AUTO_ACCEPT = 0.97
SPOT_CHECK_SHARE = 0.1


@dataclass(frozen=True)
class Region:
    box: tuple[float, float, float, float]  # x1, y1, x2, y2 as fractions of the frame
    set_at: str  # local ISO time; a camera move after it switches the region off

    @classmethod
    def from_config(cls, config: dict) -> Region | None:
        """The region in detector.json's "region" entry, or None. Raises ValueError if
        it is malformed, rather than guessing."""
        entry = config.get("region")
        if not entry:
            return None
        x1, y1, x2, y2 = (float(v) for v in entry["box"])
        if not (0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1):
            raise ValueError(f"detector region out of range: {entry['box']}")
        dt.datetime.fromisoformat(entry["set_at"])
        return cls((x1, y1, x2, y2), entry["set_at"])

    def pixels(self, shape) -> tuple[int, int, int, int]:
        h, w = shape[:2]
        x1, y1, x2, y2 = self.box
        return round(x1 * w), round(y1 * h), round(x2 * w), round(y2 * h)

    def text(self) -> str:
        x1, y1, x2, y2 = (round(100 * v) for v in self.box)
        return f"x {x1}-{x2}%, y {y1}-{y2}%"


@dataclass(frozen=True)
class Sighting:
    visit_id: int
    taken_at: dt.datetime
    ranked: list[tuple[str, float]]  # every label, most likely first
    det_conf: float
    preview_path: Path
    auto_accepted: bool = False


def last_move(store: Path, camera: str, now: dt.datetime) -> str | None:
    """When this camera was last recorded as moved, up to now (ISO), or None."""
    with closing(db.connect(store)) as conn:
        return conn.execute(
            "SELECT MAX(moved_at) FROM camera_moves WHERE camera = ? AND moved_at <= ?",
            (camera, now.isoformat(timespec="seconds")),
        ).fetchone()[0]


def not_bird_spots(store: Path, camera: str, now: dt.datetime) -> list[tuple[int, ...]]:
    """Boxes of this camera's visits answered "Not a bird" in the last SPOT_DAYS, since
    it was last moved."""
    since = (now - dt.timedelta(days=SPOT_DAYS)).isoformat(timespec="seconds")
    since = max(since, last_move(store, camera, now) or "")
    with closing(db.connect(store)) as conn:
        rows = conn.execute(
            "SELECT c.x1, c.y1, c.x2, c.y2 FROM crops c JOIN visits v ON v.id = c.visit_id "
            "JOIN current_labels l ON l.visit_id = v.id "
            "WHERE v.source = 'live' AND v.camera = ? AND l.label = ? AND v.taken_at >= ?",
            (camera, species.NOT_A_BIRD, since),
        ).fetchall()
    return [tuple(r) for r in rows]


def recently_posted(store: Path, camera: str, source: str, guess: str, now: dt.datetime) -> bool:
    """True if a visit with this first guess was recorded in the last REPEAT_WINDOW."""
    since = (now - REPEAT_WINDOW).isoformat(timespec="seconds")
    with closing(db.connect(store)) as conn:
        row = conn.execute(
            "SELECT 1 FROM visits v JOIN predictions p ON p.visit_id = v.id "
            "WHERE v.camera = ? AND v.source = ? AND p.label = ? "
            "AND v.taken_at > ? AND v.taken_at <= ? LIMIT 1",
            (camera, source, guess, since, now.isoformat(timespec="seconds")),
        ).fetchone()
    return row is not None


def detect(frame: np.ndarray, detector: Detector, region: Region | None = None) -> list[Detection]:
    """Birds in the frame (or only in the region), in full-frame pixels."""
    if region is None:
        return detector.birds(frame)
    x1, y1, x2, y2 = region.pixels(frame.shape)
    return [Detection(d.x1 + x1, d.y1 + y1, d.x2 + x1, d.y2 + y1, d.conf)
            for d in detector.birds(frame[y1:y2, x1:x2])]  # fmt: skip


def best_detection(frames: list[np.ndarray], detector: Detector, spots=(), region=None):
    """(frame index, detection, on a known spot) for the best bird in the burst, or None.
    Anything off the known not-a-bird spots beats anything on them; then confidence."""
    best = None
    for i, frame in enumerate(frames):
        for det in detect(frame, detector, region):
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
                 camera: str = "tray", source: str = "live",
                 region: Region | None = None):  # fmt: skip
        self.store, self.data_dir = store, data_dir
        self.detector, self.classifier, self.camera = detector, classifier, camera
        self.source = source  # 'test' for post-test: never trained on, never summarized
        self.rng = random.Random()  # picks the spot checks
        self.region = region
        self._region_stale_logged = False
        db.init(store)

    def current_region(self, now: dt.datetime | None = None) -> Region | None:
        """The detector region, unless the camera has moved since it was set."""
        if self.region is None:
            return None
        moved = last_move(self.store, self.camera, now or dt.datetime.now())
        if moved and moved > self.region.set_at:
            if not self._region_stale_logged:
                log.warning("detector region %s was set before the camera moved (%s); "
                            "using the whole frame", self.region.text(), moved)  # fmt: skip
                self._region_stale_logged = True
            return None
        return self.region

    def region_text(self, now: dt.datetime | None = None) -> str:
        """For status: what the detector looks at."""
        if self.region is None:
            return "whole frame"
        if self.current_region(now) is None:
            return f"whole frame (crop {self.region.text()} is from before the camera moved)"
        return f"cropped to {self.region.text()}"

    def _save(self, rel: str, image: np.ndarray, quality: int = 92) -> None:
        path = self.data_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(path), image, [cv2.IMWRITE_JPEG_QUALITY, quality])

    def process(self, frames: list[np.ndarray], now: dt.datetime | None = None) -> Sighting | None:
        now = now or dt.datetime.now()
        stamp = now.strftime("%Y-%m-%d/%H%M%S")
        spots = not_bird_spots(self.store, self.camera, now)
        found = best_detection(frames, self.detector, spots, self.current_region(now))
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
        guess, p = ranked[0]
        if recently_posted(self.store, self.camera, self.source, guess, now):
            self._save(f"rejects/{stamp}-repeat.jpg", preview(frame, det), quality=85)
            log.info("burst: repeat of %s (%.0f%%, bird %.2f)", guess, 100 * p, det.conf)
            return None
        auto = self.source == "live" and guess in POSTABLE and p >= AUTO_ACCEPT
        spot_check = auto and self.rng.random() < SPOT_CHECK_SHARE

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
            if auto:
                conn.execute(
                    "INSERT INTO auto_accepts (visit_id, spot_check, decided_at) VALUES (?, ?, ?)",
                    (visit_id, int(spot_check), now.isoformat(timespec="seconds")),
                )
            conn.commit()
        preview_rel = f"previews/{visit_id}.jpg"
        self._save(preview_rel, preview(frame, det), quality=88)
        mode = " (spot check)" if spot_check else " (auto-accepted)" if auto else ""
        log.info("visit %d: %s %.0f%% (bird %.2f)%s", visit_id, guess, 100 * p, det.conf, mode)
        return Sighting(visit_id, now, ranked, det.conf, self.data_dir / preview_rel,
                        auto and not spot_check)  # fmt: skip

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
