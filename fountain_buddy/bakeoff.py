"""Phase 3 bake-off: which frozen backbone + small head classifies OUR feeder photos best.

Everything is measured on a time split of the human-labeled legacy crops: the oldest 80%
train, the newest 20% test, so scores reflect birds the model hasn't seen. Variants:

- local:          head trained on our labels only
- local+nabirds:  plus NABirds crops at reduced weight (cold-start help)
- nabirds-only:   no local labels at all; how well NABirds alone transfers to our camera
- zero-shot:      BioCLIP 2 text prompts, no training (bird-labeled test crops only)
"""

from __future__ import annotations

import csv
import datetime as dt
from collections import Counter
from contextlib import closing
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

from fountain_buddy import db, embed, species

TEST_FRACTION = 0.2
NABIRDS_WEIGHT = 0.5
C_GRID = (0.3, 3.0, 30.0)


def labeled_crops(store: Path) -> list[tuple[int, str, str, str]]:
    """(visit_id, taken_at, label, crop_path) for every labeled visit with a crop."""
    with closing(db.connect(store)) as conn:
        return [
            tuple(r)
            for r in conn.execute(
                "SELECT v.id, v.taken_at, l.label, c.path FROM visits v "
                "JOIN current_labels l ON l.visit_id = v.id "
                "JOIN crops c ON c.visit_id = v.id AND c.method = 'drawn-box' "
                "ORDER BY v.taken_at, v.id"
            )
        ]


def time_split(rows: list, test_fraction: float = TEST_FRACTION):
    cut = int(len(rows) * (1 - test_fraction))
    return rows[:cut], rows[cut:]


def nabirds_rows(data_dir: Path) -> list[tuple[str, str]]:
    manifest = data_dir / "nabirds" / "manifest.csv"
    with open(manifest) as f:
        return [(r["species"], f"nabirds/{r['path']}") for r in csv.DictReader(f)]


def fit_head(x, y, weights=None, c: float = 3.0) -> LogisticRegression:
    head = LogisticRegression(C=c, max_iter=5000, class_weight="balanced")
    head.fit(x, y, sample_weight=weights)
    return head


def choose_c(x, y, weights=None) -> float:
    """Pick C on a time-ordered validation slice (the last 15% of the training rows)."""
    cut = int(len(y) * 0.85)
    best_c, best = C_GRID[0], -1.0
    for c in C_GRID:
        head = fit_head(x[:cut], y[:cut], None if weights is None else weights[:cut], c)
        seen = np.isin(y[cut:], head.classes_)
        score = head.score(x[cut:][seen], y[cut:][seen])
        if score > best:
            best_c, best = c, score
    return best_c


def evaluate(y_true: np.ndarray, proba: np.ndarray, classes: np.ndarray) -> dict:
    order = np.argsort(-proba, axis=1)
    top1 = classes[order[:, 0]]
    top3 = classes[order[:, :3]]
    conf = proba[np.arange(len(proba)), order[:, 0]]
    correct = top1 == y_true
    per_class = {}
    for label in sorted(set(y_true)):
        mask = y_true == label
        per_class[label] = (float(correct[mask].mean()), int(mask.sum()))
    birds = np.isin(y_true, species.SPECIES)
    bins = np.minimum((conf * 10).astype(int), 9)
    ece = sum(
        abs(correct[bins == b].mean() - conf[bins == b].mean()) * (bins == b).mean()
        for b in range(10)
        if (bins == b).any()
    )
    sure = conf >= 0.8
    skip_pred, skip_true = top1 == species.SKIP, y_true == species.SKIP
    return {
        "n": len(y_true),
        "top1": float(correct.mean()),
        "top3": float((top3 == y_true[:, None]).any(axis=1).mean()),
        "bird_top1": float(correct[birds].mean()) if birds.any() else float("nan"),
        "macro_recall": float(np.mean([v[0] for v in per_class.values()])),
        "ece": float(ece),
        "sure_share": float(sure.mean()),
        "sure_acc": float(correct[sure].mean()) if sure.any() else float("nan"),
        "skip_recall": float(skip_pred[skip_true].mean()) if skip_true.any() else float("nan"),
        "skip_precision": float(skip_true[skip_pred].mean()) if skip_pred.any() else float("nan"),
        "per_class": per_class,
    }


def run(store: Path, data_dir: Path, models: list[str]) -> str:
    rows = labeled_crops(store)
    train, test = time_split(rows)
    nab = nabirds_rows(data_dir)
    y_tr = np.array([r[2] for r in train])
    y_te = np.array([r[2] for r in test])
    y_nab = np.array([s for s, _ in nab])
    results: dict[str, dict] = {}

    for name in models:
        cache_file = data_dir / "embeddings" / f"{name}.npz"
        paths = [data_dir / r[3] for r in rows] + [data_dir / p for _, p in nab]
        feats = embed.embed_paths(name, paths, cache_file)
        x_tr, x_te = feats[: len(train)], feats[len(train) : len(rows)]
        x_nab = feats[len(rows) :]

        c = choose_c(x_tr, y_tr)
        head = fit_head(x_tr, y_tr, c=c)
        results[f"{name} local (C={c})"] = evaluate(y_te, head.predict_proba(x_te), head.classes_)

        x_mix = np.concatenate([x_tr, x_nab])
        y_mix = np.concatenate([y_tr, y_nab])
        w_mix = np.concatenate([np.ones(len(y_tr)), np.full(len(y_nab), NABIRDS_WEIGHT)])
        head = fit_head(x_mix, y_mix, w_mix, c=c)
        results[f"{name} local+nabirds"] = evaluate(y_te, head.predict_proba(x_te), head.classes_)

        birds = np.isin(y_te, species.SPECIES)
        head = fit_head(x_nab, y_nab, c=c)
        results[f"{name} nabirds-only (birds)"] = evaluate(
            y_te[birds], head.predict_proba(x_te[birds]), head.classes_
        )

        if embed.MODELS[name][0] == "open_clip":
            prompts = [f"a photo of {species.SCIENTIFIC[s]}, {s}." for s in species.SPECIES]
            text = embed.embed_texts(name, prompts)
            logits = 100 * x_te[birds] @ text.T
            proba = np.exp(logits - logits.max(axis=1, keepdims=True))
            proba /= proba.sum(axis=1, keepdims=True)
            results[f"{name} zero-shot (birds)"] = evaluate(
                y_te[birds], proba, np.array(species.SPECIES)
            )

    return report(rows, train, test, results, store)


def _v1_baseline(store: Path, test) -> tuple[int, int]:
    ids = [r[0] for r in test]
    with closing(db.connect(store)) as conn:
        preds = dict(
            conn.execute(
                f"SELECT visit_id, label FROM predictions WHERE model = 'v1-efficientnetv2b0' "
                f"AND visit_id IN ({','.join('?' * len(ids))})",
                ids,
            ).fetchall()
        )
    hits = sum(preds[r[0]] == r[2] for r in test if r[0] in preds)
    return hits, len(preds)


def report(rows, train, test, results, store: Path) -> str:
    v1_hits, v1_n = _v1_baseline(store, test)
    lines = [
        f"# Bake-off {dt.date.today().isoformat()}",
        "",
        f"Labeled crops: {len(rows)}. Train {len(train)} (through {train[-1][1][:10]}), "
        f"test {len(test)} ({test[0][1][:10]} to {test[-1][1][:10]}).",
        f"Test labels: {dict(Counter(r[2] for r in test).most_common())}",
        f"v1 baseline on test visits it scored: {v1_hits}/{v1_n}"
        + (f" = {v1_hits / v1_n:.1%}" if v1_n else ""),
        "",
        "| variant | n | top1 | top3 | birds top1 | macro recall | ECE | ≥0.8 share | ≥0.8 acc "
        "| skip recall | skip precision |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for name, m in results.items():
        lines.append(
            f"| {name} | {m['n']} | {m['top1']:.1%} | {m['top3']:.1%} | {m['bird_top1']:.1%} "
            f"| {m['macro_recall']:.1%} | {m['ece']:.3f} | {m['sure_share']:.0%} "
            f"| {m['sure_acc']:.1%} | {m['skip_recall']:.1%} | {m['skip_precision']:.1%} |"
        )
    best = max((k for k in results if "local" in k), key=lambda k: results[k]["macro_recall"])
    lines += ["", f"## Per class, {best}", "", "| label | recall | n |", "|---|---|---|"]
    for label, (recall, n) in sorted(results[best]["per_class"].items(), key=lambda kv: -kv[1][1]):
        lines.append(f"| {label} | {recall:.1%} | {n} |")
    return "\n".join(lines) + "\n"


DETECTOR_CONFIGS = (
    ("yolov8n.pt", 640),  # v1's detector
    ("yolo26n.pt", 640),
    ("yolo26s.pt", 640),
    ("yolo26s.pt", 1280),
    ("yolo26m.pt", 1280),
)


def detection_recall(store: Path, data_dir: Path, sample: int = 400, seed: int = 7) -> str:
    """For labeled bird photos, how often does each detector find the bird the human
    labeled (IoU >= 0.3 with v1's drawn box)? Also time per 4K frame."""
    import random
    import time

    import cv2

    from fountain_buddy.detect import Detector, iou

    with closing(db.connect(store)) as conn:
        rows = conn.execute(
            "SELECT v.image_path, c.x1, c.y1, c.x2, c.y2 FROM visits v "
            "JOIN current_labels l ON l.visit_id = v.id "
            "JOIN crops c ON c.visit_id = v.id AND c.method = 'drawn-box' "
            f"WHERE l.label IN ({','.join('?' * len(species.SPECIES))})",
            species.SPECIES,
        ).fetchall()
    random.Random(seed).shuffle(rows)
    rows = rows[:sample]
    frames = [(cv2.imread(str(data_dir / r[0])), tuple(r[1:])) for r in rows]

    lines = [
        f"# Detector recall {dt.date.today().isoformat()}",
        "",
        f"{len(frames)} labeled bird photos (4K). Hit = a bird box with IoU >= 0.3 against the "
        "box v1 drew (the drawn box is in the image for every detector alike).",
        "",
        "| detector | recall | top-1 is the labeled bird | ms/frame |",
        "|---|---|---|---|",
    ]
    for weights, imgsz in DETECTOR_CONFIGS:
        det = Detector(data_dir / "models", weights, imgsz)
        det.birds(frames[0][0])  # warm-up
        hits = top_hits = 0
        start = time.perf_counter()
        for frame, box in frames:
            found = [iou(box, (d.x1, d.y1, d.x2, d.y2)) for d in det.birds(frame)]
            hits += any(v >= 0.3 for v in found)
            top_hits += bool(found) and found[0] >= 0.3
        ms = 1000 * (time.perf_counter() - start) / len(frames)
        n = len(frames)
        lines.append(f"| {det.name} | {hits / n:.1%} | {top_hits / n:.1%} | {ms:.0f} |")
    return "\n".join(lines) + "\n"
