"""Fine-tune a YOLO bird detector on our own verified boxes.

Source: v1's labeled frames. The box v1 drew around each bird is the label (recovered
in `legacy.extract_crops`), and the drawing itself is painted out of the frame first
(`legacy.remove_overlays`) so the detector can't learn "green rectangle means bird".
Other birds in the same frame, found by a stock model at high confidence, are added as
boxes too, so they aren't taught as background.

Split by time like the classifier: oldest 80% train (the last 15% of that is val),
newest 20% test.
"""

from __future__ import annotations

import datetime as dt
import random
import time
from contextlib import closing
from pathlib import Path

import cv2

from fountain_buddy import db, legacy, species
from fountain_buddy.detect import Detection, Detector, iou

SCALE = 0.5  # store 1920x1080; the detector runs at 1280 anyway
PSEUDO_CONF = 0.5


def _rows(store: Path):
    q = ",".join("?" * len(species.SPECIES))
    with closing(db.connect(store)) as conn:
        return conn.execute(
            "SELECT v.id, v.taken_at, v.image_path, c.x1, c.y1, c.x2, c.y2 FROM visits v "
            "JOIN current_labels l ON l.visit_id = v.id "
            "JOIN crops c ON c.visit_id = v.id AND c.method = 'drawn-box' "
            f"WHERE l.label IN ({q}) ORDER BY v.taken_at, v.id",
            species.SPECIES,
        ).fetchall()


def _yolo_line(box, w: int, h: int) -> str:
    x1, y1, x2, y2 = box
    return (
        f"0 {(x1 + x2) / 2 / w:.6f} {(y1 + y2) / 2 / h:.6f} {(x2 - x1) / w:.6f} {(y2 - y1) / h:.6f}"
    )


def build_dataset(store: Path, data_dir: Path) -> Path:
    """Write data/detector/{images,labels}/{train,val,test} and data.yaml. Idempotent."""
    out = data_dir / "detector"
    rows = _rows(store)
    cut = int(len(rows) * 0.8)
    val_cut = int(cut * 0.85)
    splits = {"train": rows[:val_cut], "val": rows[val_cut:cut], "test": rows[cut:]}
    stock = Detector(data_dir / "models", "yolo26m.pt", 1280, conf=PSEUDO_CONF)
    pseudo = 0
    for split, items in splits.items():
        (out / "images" / split).mkdir(parents=True, exist_ok=True)
        (out / "labels" / split).mkdir(parents=True, exist_ok=True)
        for visit_id, _, rel, x1, y1, x2, y2 in items:
            img_path = out / "images" / split / f"{visit_id}.jpg"
            label_path = out / "labels" / split / f"{visit_id}.txt"
            if img_path.exists() and label_path.exists():
                continue
            frame = cv2.imread(str(data_dir / rel))
            if frame is None:
                continue
            clean = legacy.remove_overlays(frame)
            i = legacy.INSET  # crops are stored inset from the drawn box
            boxes = [(x1 - i, y1 - i, x2 + i, y2 + i)]
            for d in stock.birds(clean):
                if all(iou(b, (d.x1, d.y1, d.x2, d.y2)) < 0.1 for b in boxes):
                    boxes.append((d.x1, d.y1, d.x2, d.y2))
                    pseudo += 1
            small = cv2.resize(clean, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_AREA)
            h, w = small.shape[:2]
            cv2.imwrite(str(img_path), small, [cv2.IMWRITE_JPEG_QUALITY, 92])
            label_path.write_text(
                "\n".join(_yolo_line([v * SCALE for v in b], w, h) for b in boxes) + "\n"
            )
    # Remove frames left over from an earlier split assignment.
    for split, items in splits.items():
        keep = {str(r[0]) for r in items}
        for sub in ("images", "labels"):
            for f in (out / sub / split).iterdir():
                if f.stem not in keep:
                    f.unlink()
    yaml = out / "data.yaml"
    yaml.write_text(
        f"path: {out}\ntrain: images/train\nval: images/val\ntest: images/test\nnames:\n  0: bird\n"
    )
    print(f"detector dataset: { {k: len(v) for k, v in splits.items()} }, +{pseudo} extra birds")
    return yaml


def train(data_dir: Path, base: str = "yolo26s.pt", imgsz: int = 1280, epochs: int = 60) -> Path:
    from ultralytics import YOLO

    from fountain_buddy.embed import device

    name = f"{Path(base).stem}-{imgsz}-{dt.datetime.now():%Y%m%d-%H%M}"
    model = YOLO(str(data_dir / "models" / base))
    model.train(
        data=str(data_dir / "detector" / "data.yaml"),
        imgsz=imgsz,
        epochs=epochs,
        patience=15,
        batch=8,
        device=device(),
        project=str(data_dir / "detector" / "runs"),
        name=name,
        workers=4,
        seed=7,
        plots=False,
    )
    best = data_dir / "detector" / "runs" / name / "weights" / "best.pt"
    print(f"best weights: {best}")
    return best


def evaluate(data_dir: Path, weights: list[Path], imgsz: int = 1280) -> str:
    """Recall of the labeled bird (first box in each test label file) and stray boxes per
    frame, on the held-out test frames, at several confidence cutoffs."""
    test_dir = data_dir / "detector" / "images" / "test"
    items = []
    for img_path in sorted(test_dir.glob("*.jpg")):
        frame = cv2.imread(str(img_path))
        h, w = frame.shape[:2]
        first = (data_dir / "detector" / "labels" / "test" / f"{img_path.stem}.txt").read_text()
        _, cx, cy, bw, bh = (float(v) for v in first.split("\n")[0].split())
        box = (int((cx - bw / 2) * w), int((cy - bh / 2) * h),
               int((cx + bw / 2) * w), int((cy + bh / 2) * h))  # fmt: skip
        items.append((frame, box))
    random.Random(7).shuffle(items)
    cutoffs = (0.5, 0.25, 0.1)
    lines = [
        f"# Fine-tuned detector eval {dt.date.today().isoformat()}",
        "",
        f"{len(items)} held-out test frames (newest 20%, overlays painted out, 1920x1080).",
        "Recall = the labeled bird found (IoU >= 0.3). Stray = boxes per frame overlapping "
        "no labeled bird.",
        "",
        "| detector | " + " | ".join(f"recall @{c} | stray @{c}" for c in cutoffs) + " | ms |",
        "|---|" + "---|---|" * len(cutoffs) + "---|",
    ]
    for wpath in weights:
        det = Detector(wpath.parent, wpath.name, imgsz, conf=min(cutoffs))
        det.name = f"{wpath.parent.parent.name if wpath.name == 'best.pt' else wpath.stem}"
        det.birds(items[0][0])
        hits = dict.fromkeys(cutoffs, 0)
        stray = dict.fromkeys(cutoffs, 0)
        start = time.perf_counter()
        for frame, box in items:
            dets: list[Detection] = det.birds(frame)
            for c in cutoffs:
                kept = [d for d in dets if d.conf >= c]
                hits[c] += any(iou(box, (d.x1, d.y1, d.x2, d.y2)) >= 0.3 for d in kept)
                stray[c] += sum(iou(box, (d.x1, d.y1, d.x2, d.y2)) < 0.1 for d in kept)
        ms = 1000 * (time.perf_counter() - start) / len(items)
        n = len(items)
        cells = " | ".join(f"{hits[c] / n:.1%} | {stray[c] / n:.2f}" for c in cutoffs)
        lines.append(f"| {det.name} | {cells} | {ms:.0f} |")
    return "\n".join(lines) + "\n"
