"""Species classifier: frozen BioCLIP 2 features, a logistic-regression head trained on
our labels plus NABirds, blended with BioCLIP 2 zero-shot (the Phase 3 choice; numbers
in AGENTS.md, "Model choices").

The head is a joblib file in data/models/; data/models/head.json names the current one.
`Classifier` reloads when head.json changes, so retraining needs no restart.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
from contextlib import closing
from pathlib import Path

import cv2
import joblib
import numpy as np
from PIL import Image

from fountain_buddy import bakeoff, db, embed, species

log = logging.getLogger(__name__)

BACKBONE = "bioclip2"
NABIRDS_WEIGHT = 0.5
C = 30.0
ZERO_SHOT_ALPHA = 0.3


def _prompts() -> list[str]:
    return [f"a photo of {species.SCIENTIFIC[s]}, {s}." for s in species.SPECIES]


def blend_zero_shot(proba: np.ndarray, classes: list[str], zs: np.ndarray) -> np.ndarray:
    """Mix zero-shot into the species part of the head's distribution (geometric mean,
    weight ZERO_SHOT_ALPHA). Non-species mass (Skip, Not a bird, Squirrel) is kept."""
    out = proba.copy()
    cols = [classes.index(s) for s in species.SPECIES if s in classes]
    zcols = [i for i, s in enumerate(species.SPECIES) if s in classes]
    mass = out[:, cols].sum(axis=1, keepdims=True)
    mix = (out[:, cols] / np.maximum(mass, 1e-9)) ** (1 - ZERO_SHOT_ALPHA) * zs[
        :, zcols
    ] ** ZERO_SHOT_ALPHA
    mix /= mix.sum(axis=1, keepdims=True)
    out[:, cols] = mix * mass
    return out


def training_rows(store: Path) -> list[tuple[int, str, str, str]]:
    """(visit_id, taken_at, label, crop_path) for every labeled visit with a crop, oldest
    first. Live visits use their detector crop; legacy ones the recovered drawn box."""
    with closing(db.connect(store)) as conn:
        rows = conn.execute(
            "SELECT v.id, v.taken_at, l.label, c.path FROM visits v "
            "JOIN current_labels l ON l.visit_id = v.id "
            "JOIN crops c ON c.id = (SELECT MIN(id) FROM crops WHERE visit_id = v.id) "
            "WHERE v.source != 'test' "
            "ORDER BY v.taken_at, v.id"
        ).fetchall()
    return [tuple(r) for r in rows if r[2] in species.LABELS]


def train_head(store: Path, data_dir: Path) -> Path:
    """Fit a head on every label plus NABirds, report its time-split score, and make it
    current."""
    rows = training_rows(store)
    nab = bakeoff.nabirds_rows(data_dir)
    paths = [data_dir / r[3] for r in rows] + [data_dir / p for _, p in nab]
    feats = embed.embed_paths(BACKBONE, paths, data_dir / "embeddings" / f"{BACKBONE}.npz")
    x_local, x_nab = feats[: len(rows)], feats[len(rows) :]
    y_local = np.array([r[2] for r in rows])
    y_nab = np.array([s for s, _ in nab])

    # Held-out score first (oldest 80% -> newest 20%), for the record and for gating.
    cut = int(len(rows) * 0.8)
    zs_text = embed.embed_texts(BACKBONE, _prompts())
    held = bakeoff.fit_head(
        np.concatenate([x_local[:cut], x_nab]),
        np.concatenate([y_local[:cut], y_nab]),
        np.concatenate([np.ones(cut), np.full(len(y_nab), NABIRDS_WEIGHT)]),
        c=C,
    )
    proba = blend_zero_shot(
        held.predict_proba(x_local[cut:]), list(held.classes_), _zero_shot(x_local[cut:], zs_text)
    )
    metrics = bakeoff.evaluate(y_local[cut:], proba, held.classes_)
    metrics.pop("per_class")

    head = bakeoff.fit_head(
        np.concatenate([x_local, x_nab]),
        np.concatenate([y_local, y_nab]),
        np.concatenate([np.ones(len(y_local)), np.full(len(y_nab), NABIRDS_WEIGHT)]),
        c=C,
    )
    models = data_dir / "models"
    name = f"head-{dt.datetime.now():%Y%m%d-%H%M%S}.joblib"
    joblib.dump({"head": head, "zs_text": zs_text, "backbone": BACKBONE}, models / name)
    (models / "head.json").write_text(
        json.dumps(
            {
                "head": name,
                "trained_at": dt.datetime.now().isoformat(timespec="seconds"),
                "labels": len(rows),
                "nabirds": len(nab),
                "heldout": metrics,
            },
            indent=2,
        )  # fmt: skip
    )
    log.info(
        "trained %s on %d labels: held-out top1 %.1f%%", name, len(rows), 100 * metrics["top1"]
    )
    return models / name


def _zero_shot(feats: np.ndarray, text: np.ndarray) -> np.ndarray:
    logits = 100 * feats @ text.T
    z = np.exp(logits - logits.max(axis=1, keepdims=True))
    return z / z.sum(axis=1, keepdims=True)


class Classifier:
    def __init__(self, models_dir: Path):
        self.models_dir = models_dir
        self._stamp: float | None = None
        self._bundle: dict | None = None

    @property
    def version(self) -> str:
        self._maybe_reload()
        return json.loads((self.models_dir / "head.json").read_text())["head"]

    def _maybe_reload(self) -> None:
        pointer = self.models_dir / "head.json"
        stamp = pointer.stat().st_mtime
        if stamp != self._stamp:
            name = json.loads(pointer.read_text())["head"]
            self._bundle = joblib.load(self.models_dir / name)
            self._stamp = stamp
            log.info("classifier: loaded %s", name)

    def predict(self, crop_bgr: np.ndarray) -> list[tuple[str, float]]:
        """All labels, most likely first."""
        self._maybe_reload()
        head, text = self._bundle["head"], self._bundle["zs_text"]
        image = Image.fromarray(cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB))
        feats = embed.embed_images(BACKBONE, [image])
        proba = blend_zero_shot(
            head.predict_proba(feats), list(head.classes_), _zero_shot(feats, text)
        )
        order = np.argsort(-proba[0])
        return [(str(head.classes_[i]), float(proba[0][i])) for i in order]
