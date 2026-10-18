"""Cold-start data from NABirds (Cornell, non-commercial use; never redistributed here).

Extracts bounding-box crops for the species in `species.SPECIES`, folding NABirds'
variant classes ("Northern Cardinal (Adult Male)") into the base species. Our own
photos always outrank these; they exist for species with few or no local labels.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

import cv2

from fountain_buddy import species


def _read(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text().splitlines():
        key, _, rest = line.partition(" ")
        out[key] = rest
    return out


def base_species(class_name: str) -> str | None:
    return species.canonical(re.sub(r"\s*\(.*\)$", "", class_name))


def extract(source: Path, out_dir: Path) -> dict[str, int]:
    """Write crops to out_dir/<Species_Name>/<image_id>.jpg plus manifest.csv. Idempotent."""
    classes = _read(source / "classes.txt")
    images = _read(source / "images.txt")
    labels = _read(source / "image_class_labels.txt")
    boxes = _read(source / "bounding_boxes.txt")

    counts: dict[str, int] = {}
    rows = []
    for image_id, class_id in labels.items():
        name = base_species(classes[class_id])
        if name is None:
            continue
        rel = images[image_id]
        src = source / "images" / rel
        if not src.exists():
            src = src.with_suffix(".JPG")
        dest = out_dir / name.replace(" ", "_") / f"{image_id}.jpg"
        if not dest.exists():
            img = cv2.imread(str(src))
            if img is None:
                continue
            x, y, w, h = (int(v) for v in boxes[image_id].split())
            crop = img[max(y, 0) : y + h, max(x, 0) : x + w]
            if crop.size == 0:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(dest), crop, [cv2.IMWRITE_JPEG_QUALITY, 95])
        rows.append((name, str(dest.relative_to(out_dir)), image_id))
        counts[name] = counts.get(name, 0) + 1

    with open(out_dir / "manifest.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["species", "path", "nabirds_id"])
        writer.writerows(sorted(rows))
    return counts
