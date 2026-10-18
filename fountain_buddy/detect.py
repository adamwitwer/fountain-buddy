"""Bird detection with Ultralytics YOLO (COCO class 14, "bird").

Weights live in data/models/ (never the repo root, where Ultralytics would otherwise
download them).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from fountain_buddy.embed import device

COCO_BIRD = 14


@dataclass(frozen=True)
class Detection:
    x1: int
    y1: int
    x2: int
    y2: int
    conf: float

    @property
    def area(self) -> int:
        return (self.x2 - self.x1) * (self.y2 - self.y1)


class Detector:
    def __init__(self, models_dir: Path, weights: str = "yolo26s.pt", imgsz: int = 1280,
                 conf: float = 0.25):  # fmt: skip
        from ultralytics import YOLO

        models_dir.mkdir(parents=True, exist_ok=True)
        self.name = f"{Path(weights).stem}@{imgsz}"
        self.model = YOLO(str(models_dir / weights))
        self.imgsz, self.conf = imgsz, conf

    def birds(self, frame: np.ndarray) -> list[Detection]:
        """Bird detections in a BGR frame, most confident first."""
        result = self.model.predict(
            frame, imgsz=self.imgsz, conf=self.conf, classes=[COCO_BIRD],
            device=device(), verbose=False,
        )[0]  # fmt: skip
        dets = [
            Detection(*(int(v) for v in box.xyxy[0].tolist()), float(box.conf[0]))
            for box in result.boxes
        ]
        return sorted(dets, key=lambda d: -d.conf)


def iou(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union else 0.0
