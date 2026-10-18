import sqlite3

import cv2
import numpy as np

from fountain_buddy import db, legacy


def _frame_with_box(box, foliage=False):
    rng = np.random.default_rng(0)
    img = rng.integers(60, 140, size=(720, 1280, 3), dtype=np.uint8)
    if foliage:  # a pure-green blob touching the box's left side, like a sunlit leaf
        cv2.circle(img, (box[0] - 20, (box[1] + box[3]) // 2), 40, (0, 220, 0), -1)
    cv2.rectangle(img, box[:2], box[2:], (0, 255, 0), 2)
    cv2.putText(img, "Bird 0.81", (box[0], box[1] - 10), 0, 0.5, (0, 255, 0), 2)
    ok, jpg = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return cv2.imdecode(jpg, cv2.IMREAD_COLOR)


def test_find_drawn_box_through_jpeg():
    found = legacy.find_drawn_box(_frame_with_box((400, 200, 640, 380)))
    assert found is not None
    assert all(type(v) is int for v in found)  # numpy ints become BLOBs in SQLite
    assert all(abs(a - b) <= 2 for a, b in zip(found, (400, 200, 640, 380), strict=True))


def test_find_drawn_box_touching_foliage():
    found = legacy.find_drawn_box(_frame_with_box((400, 200, 640, 380), foliage=True))
    assert found is not None
    assert all(abs(a - b) <= 2 for a, b in zip(found, (400, 200, 640, 380), strict=True))


def test_find_drawn_box_none():
    rng = np.random.default_rng(1)
    assert legacy.find_drawn_box(rng.integers(0, 255, (360, 640, 3), dtype=np.uint8)) is None


def _legacy_db(path):
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE bird_visits (id INTEGER PRIMARY KEY, timestamp TEXT, bird_type TEXT, "
        "image_path TEXT, species TEXT, confidence REAL, location TEXT, camera_id TEXT, "
        "ai_species TEXT, review_status TEXT)"
    )
    rows = [
        # human label (legacy spelling), model guess
        (1, "2025-07-01 14:04:44", "bird_images/active/a.jpg", "Blue_Jay", 1.0, "fountain",
         "Downy Woodpecker", None),
        # model guess only: not a label
        (2, "2025-08-01 09:00:00", "bird_images/peanut/b.jpg", "House Sparrow", 0.42, "peanut",
         "House Sparrow", None),
        # human skip
        (3, "2025-09-01 09:00:00", "bird_images/archive/c.jpg", None, None, "peanut",
         "Tufted Titmouse", "archived_poor_quality"),
        # December 'fountain' was really the peanut feeder camera
        (4, "2025-12-26 15:25:19", "bird_images/fountain/d.jpg", None, None, "fountain",
         "Unknown Bird", None),
    ]  # fmt: skip
    conn.executemany(
        "INSERT INTO bird_visits (id, timestamp, image_path, species, confidence, location, "
        "ai_species, review_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    conn.close()


def test_import_visits(tmp_path):
    old, store = tmp_path / "legacy.db", tmp_path / "fb.db"
    _legacy_db(old)
    counts = legacy.import_visits(old, store)
    assert counts == {"visits": 4, "labels": 2, "predictions": 3, "skipped": 0}

    conn = db.connect(store)
    labels = dict(
        conn.execute(
            "SELECT v.legacy_id, l.label FROM current_labels l JOIN visits v ON v.id = l.visit_id"
        ).fetchall()
    )
    assert labels == {1: "Blue Jay", 3: "Skip"}
    cameras = dict(conn.execute("SELECT legacy_id, camera FROM visits").fetchall())
    assert cameras[1] == "legacy-fountain" and cameras[4] == "legacy-peanut"
    path = conn.execute("SELECT image_path FROM visits WHERE legacy_id = 1").fetchone()[0]
    assert path == "images/active/a.jpg"

    assert legacy.import_visits(old, store)["skipped"] == 4  # idempotent


def test_iou():
    from fountain_buddy.detect import iou

    assert iou((0, 0, 10, 10), (0, 0, 10, 10)) == 1.0
    assert iou((0, 0, 10, 10), (20, 20, 30, 30)) == 0.0
    assert abs(iou((0, 0, 10, 10), (5, 0, 15, 10)) - 1 / 3) < 1e-9


def test_remove_overlays_erases_the_box():
    img = _frame_with_box((400, 200, 640, 380), foliage=True)
    clean = legacy.remove_overlays(img)
    assert legacy.find_drawn_box(img) is not None
    assert legacy.find_drawn_box(clean) is None
    b, g, r = (clean[:, :, i].astype(int) for i in range(3))
    assert ((g > 160) & (r < 110) & (b < 110))[195:205, 400:640].mean() < 0.05


def test_find_drawn_box_ignores_tiny_squares():
    img = _frame_with_box((400, 200, 640, 380))
    cv2.rectangle(img, (900, 500), (920, 520), (0, 255, 0), 2)  # a foliage-sized square
    found = legacy.find_drawn_box(img)
    assert found is not None and found[0] < 450
    small_only = _frame_with_box((400, 200, 430, 230))
    assert legacy.find_drawn_box(small_only) is None
