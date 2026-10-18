"""One-time rescue of v1's data: import its visits and human labels, and cut clean crops.

v1 drew the winning YOLO box (pure green, 2 px) into every saved frame, and the human
labeled that photo. So the drawn box is the most faithful record of which bird a label
refers to: we find it by color and crop just inside it.
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

import cv2
import numpy as np

from fountain_buddy import db, species

# v1 posted Dec 2025 photos from the .249 camera as 'fountain', but by then that camera
# was at the peanut feeder (its overlay says "Peanut Feeder").
_PEANUT_FROM = "2025-12-01"

# Inset from the drawn box so the 2 px line and its JPEG bleed stay out of the crop.
INSET = 4
# v1's real boxes are all >= 100 px on their short side in 4K frames; anything under
# 40 px is a square of green foliage (12 such false finds on 2026-10-18).
MIN_SIDE = 40


def _camera(location: str | None, taken_at: str) -> str:
    if location == "fountain" and taken_at >= _PEANUT_FROM:
        return "legacy-peanut"
    return f"legacy-{location or 'fountain'}"


def _human_label(species_name: str | None, confidence: float | None, review: str | None):
    """v1 marked a human answer with confidence 1.0; a 'skip' reply cleared the species
    and set review_status. Anything else was the model's guess, not a label."""
    if review == "archived_poor_quality":
        return species.SKIP
    if confidence == 1.0 and species_name:
        label = species.canonical(species_name)
        if label is None:
            raise ValueError(f"unmapped legacy label {species_name!r}")
        return label
    return None


def import_visits(legacy_db: Path, store: Path) -> dict[str, int]:
    """Copy v1's visits, human labels and v1 predictions into the new store.
    Idempotent: rows already imported (by legacy_id) are skipped."""
    db.init(store)
    counts = {"visits": 0, "labels": 0, "predictions": 0, "skipped": 0}
    with closing(sqlite3.connect(legacy_db)) as old, closing(db.connect(store)) as new:
        rows = old.execute(
            "SELECT id, timestamp, image_path, species, confidence, location, ai_species, "
            "review_status FROM bird_visits ORDER BY id"
        ).fetchall()
        for lid, taken_at, image_path, name, conf, location, ai, review in rows:
            if new.execute("SELECT 1 FROM visits WHERE legacy_id = ?", (lid,)).fetchone():
                counts["skipped"] += 1
                continue
            rel = image_path.replace("bird_images/", "images/", 1) if image_path else None
            cur = new.execute(
                "INSERT INTO visits (taken_at, camera, image_path, frame_marked, source, "
                "legacy_id) VALUES (?, ?, ?, 1, 'legacy', ?)",
                (taken_at.replace(" ", "T"), _camera(location, taken_at), rel, lid),
            )
            visit_id = cur.lastrowid
            counts["visits"] += 1
            label = _human_label(name, conf, review)
            if label:
                new.execute(
                    "INSERT INTO labels (visit_id, label, source, labeled_at) "
                    "VALUES (?, ?, 'legacy', ?)",
                    (visit_id, label, taken_at.replace(" ", "T")),
                )
                counts["labels"] += 1
            if ai and ai != "Unknown Bird" and species.canonical(ai):
                new.execute(
                    "INSERT INTO predictions (visit_id, model, label, predicted_at) "
                    "VALUES (?, 'v1-efficientnetv2b0', ?, ?)",
                    (visit_id, species.canonical(ai), taken_at.replace(" ", "T")),
                )
                counts["predictions"] += 1
        new.commit()
    return counts


def _green_masks(img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(pure-green pixels, the straight horizontal/vertical runs among them).
    Keeping only straight runs stops a box that touches green foliage from merging with
    it into one blob."""
    b, g, r = cv2.split(img)
    green = ((g > 160) & (r < 110) & (b < 110)).astype(np.uint8)
    green = cv2.morphologyEx(green, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    lines = cv2.morphologyEx(green, cv2.MORPH_OPEN, np.ones((1, 15), np.uint8)) | (
        cv2.morphologyEx(green, cv2.MORPH_OPEN, np.ones((15, 1), np.uint8))
    )
    return green, lines


def remove_overlays(img: np.ndarray) -> np.ndarray:
    """Paint out v1's drawn boxes and the label text above them, so a detector trained
    on these frames can't learn "green rectangle means bird"."""
    green, lines = _green_masks(img)
    mask = cv2.dilate(lines, np.ones((5, 5), np.uint8))
    n, _, stats, _ = cv2.connectedComponentsWithStats(lines, connectivity=8)
    h, w = green.shape
    for i in range(1, n):
        x, y = stats[i][0], stats[i][1]
        # v1 wrote "<label> <conf>" at (x1, y1 - 10) in small green type.
        y0, x1 = max(0, y - 40), min(w, x + 320)
        mask[y0 : y + 3, max(0, x - 3) : x1] |= green[y0 : y + 3, max(0, x - 3) : x1]
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))
    return cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)


def find_drawn_box(img: np.ndarray) -> tuple[int, int, int, int] | None:
    """Find v1's green box in a BGR frame. Returns (x1, y1, x2, y2) of the line centers,
    or None. Picks the largest hollow green rectangle; the label text above it and
    green foliage don't form one."""
    mask = cv2.dilate(_green_masks(img)[1], np.ones((3, 3), np.uint8))
    n, _, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    best, best_area = None, 0
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if w < MIN_SIDE or h < MIN_SIDE or area > 0.5 * w * h:
            continue
        sub = mask[y : y + h, x : x + w]
        rows = np.flatnonzero(sub.mean(axis=1) > 0.6)
        cols = np.flatnonzero(sub.mean(axis=0) > 0.6)
        if len(rows) < 2 or len(cols) < 2:
            continue
        top, bottom, left, right = rows[0], rows[-1], cols[0], cols[-1]
        if bottom - top < MIN_SIDE or right - left < MIN_SIDE:
            continue
        # The vertical sides must run the full height between the horizontal lines.
        span = sub[top : bottom + 1]
        if span[:, left].mean() < 0.8 or span[:, right].mean() < 0.8:
            continue
        # Plain ints: SQLite stores numpy integers as 8-byte BLOBs.
        box = tuple(int(v) for v in (x + left, y + top, x + right, y + bottom))
        box_area = (box[2] - box[0]) * (box[3] - box[1])
        if box_area > best_area:
            best, best_area = box, box_area
    return best


def extract_crops(store: Path, data_dir: Path, labeled_only: bool = True) -> dict[str, int]:
    """Cut a crop inside the drawn box for each imported visit. Idempotent."""
    counts = {"cropped": 0, "no_box": 0, "missing_image": 0, "skipped": 0}
    out_dir = data_dir / "crops" / "legacy"
    out_dir.mkdir(parents=True, exist_ok=True)
    query = (
        "SELECT v.id, v.image_path FROM visits v "
        + ("JOIN current_labels l ON l.visit_id = v.id " if labeled_only else "")
        + "WHERE v.source = 'legacy' AND NOT EXISTS "
        "(SELECT 1 FROM crops c WHERE c.visit_id = v.id AND c.method = 'drawn-box')"
    )
    with closing(db.connect(store)) as conn:
        for visit_id, rel in conn.execute(query).fetchall():
            img = cv2.imread(str(data_dir / rel)) if rel else None
            if img is None:
                counts["missing_image"] += 1
                continue
            box = find_drawn_box(img)
            if box is None:
                counts["no_box"] += 1
                continue
            x1, y1, x2, y2 = box[0] + INSET, box[1] + INSET, box[2] - INSET, box[3] - INSET
            crop_rel = f"crops/legacy/{visit_id}.jpg"
            cv2.imwrite(str(data_dir / crop_rel), img[y1:y2, x1:x2], [cv2.IMWRITE_JPEG_QUALITY, 95])
            conn.execute(
                "INSERT INTO crops (visit_id, method, x1, y1, x2, y2, path) "
                "VALUES (?, 'drawn-box', ?, ?, ?, ?, ?)",
                (visit_id, x1, y1, x2, y2, crop_rel),
            )
            counts["cropped"] += 1
            if counts["cropped"] % 250 == 0:
                conn.commit()
        conn.commit()
    return counts
