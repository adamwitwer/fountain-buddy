"""Species classifier: frozen BioCLIP 2 features, a logistic-regression head trained on
our labels plus NABirds, blended with BioCLIP 2 zero-shot (the Phase 3 choice; numbers
in AGENTS.md, "Model choices").

The head is a joblib file in data/models/; data/models/head.json names the current one.
`Classifier` reloads when head.json changes, so retraining needs no restart.

`retrain` is the learning loop (Phase 5). A new head replaces the current one only if it
does at least as well on the gate set: the newest 20% of the labels the current head
already had. Both are fit without those rows, the incumbent on its own labels and the
candidate on every label, so the comparison asks one question: do the new answers make
the model worse on photos neither model has seen?
"""

from __future__ import annotations

import datetime as dt
import json
import logging
from contextlib import closing
from dataclasses import dataclass
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
TEST_FRACTION = 0.2
# A few new labels move top-1 by a crop or two either way; half a point is that noise.
GATE_TOLERANCE = 0.005
GATE_METRICS = ("top1", "top3")
KEEP_HEADS = 10


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


def training_rows(store: Path) -> list[tuple[int, str, str, str, int]]:
    """(visit_id, taken_at, label, crop_path, label_id) for every labeled visit with a
    crop, oldest first. Live visits use their detector crop; legacy ones the recovered
    drawn box. TEST posts and labels outside species.LABELS (a typed new species) are
    left out."""
    with closing(db.connect(store)) as conn:
        rows = conn.execute(
            "SELECT v.id, v.taken_at, l.label, c.path, l.id FROM visits v "
            "JOIN current_labels l ON l.visit_id = v.id "
            "JOIN crops c ON c.id = (SELECT MIN(id) FROM crops WHERE visit_id = v.id) "
            "WHERE v.source != 'test' "
            "ORDER BY v.taken_at, v.id"
        ).fetchall()
    return [tuple(r) for r in rows if r[2] in species.LABELS]


def gate_split(label_ids: np.ndarray, incumbent_max: int) -> tuple[np.ndarray, np.ndarray]:
    """Row indices (time order) of (the incumbent's training rows, the gate test rows).
    The gate set is the newest TEST_FRACTION of the rows the incumbent already had."""
    known = np.flatnonzero(label_ids <= incumbent_max)
    cut = int(len(known) * (1 - TEST_FRACTION))
    return known[:cut], known[cut:]


def passes(candidate: dict, incumbent: dict) -> bool:
    return all(candidate[k] >= incumbent[k] - GATE_TOLERANCE for k in GATE_METRICS)


@dataclass
class Retrain:
    accepted: bool
    reason: str
    head: str | None  # the current head afterwards
    new_labels: int
    gate: dict | None = None


def _zero_shot(feats: np.ndarray, text: np.ndarray) -> np.ndarray:
    logits = 100 * feats @ text.T
    z = np.exp(logits - logits.max(axis=1, keepdims=True))
    return z / z.sum(axis=1, keepdims=True)


def _fit(x, y, x_nab, y_nab):
    return bakeoff.fit_head(
        np.concatenate([x, x_nab]),
        np.concatenate([y, y_nab]),
        np.concatenate([np.ones(len(y)), np.full(len(y_nab), NABIRDS_WEIGHT)]),
        c=C,
    )


def _score(head, x_test, y_test, zs_text) -> dict:
    proba = blend_zero_shot(
        head.predict_proba(x_test), list(head.classes_), _zero_shot(x_test, zs_text)
    )
    metrics = bakeoff.evaluate(y_test, proba, head.classes_)
    metrics.pop("per_class")
    return metrics


def _incumbent_max_label(store: Path, current: dict | None) -> int:
    if current is None:
        return 0
    if "max_label_id" in current:
        return current["max_label_id"]
    # head.json from before Phase 5: the labels that existed when it was trained.
    with closing(db.connect(store)) as conn:
        row = conn.execute(
            "SELECT MAX(id) FROM labels WHERE labeled_at <= ?", (current["trained_at"],)
        ).fetchone()
    return row[0] or 0


def _record(store: Path, result: Retrain, labels: int, max_label_id: int) -> None:
    with closing(db.connect(store)) as conn:
        conn.execute(
            "INSERT INTO trainings (trained_at, head, accepted, labels, new_labels, "
            "max_label_id, gate, reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (dt.datetime.now().isoformat(timespec="seconds"),
             result.head if result.accepted else None, int(result.accepted), labels,
             result.new_labels, max_label_id,
             json.dumps(result.gate) if result.gate else None, result.reason),
        )  # fmt: skip
        conn.commit()


def _prune(models: Path, keep: str) -> None:
    heads = sorted(models.glob("head-*.joblib"))
    for old in heads[:-KEEP_HEADS]:
        if old.name != keep:
            old.unlink()


def retrain(store: Path, data_dir: Path, force: bool = False) -> Retrain:
    """Fit a head on every label plus NABirds and make it current if it passes the gate.
    Does nothing when no label has arrived since the current head (unless forced)."""
    models = data_dir / "models"
    pointer = models / "head.json"
    current = json.loads(pointer.read_text()) if pointer.exists() else None
    rows = training_rows(store)
    ids = np.array([r[4] for r in rows])
    incumbent_max = _incumbent_max_label(store, current)
    new = int((ids > incumbent_max).sum())
    current_head = current["head"] if current else None
    if not new and not force:
        return Retrain(False, "no new labels", current_head, 0)

    nab = bakeoff.nabirds_rows(data_dir)
    paths = [data_dir / r[3] for r in rows] + [data_dir / p for _, p in nab]
    feats = embed.embed_paths(BACKBONE, paths, data_dir / "embeddings" / f"{BACKBONE}.npz")
    x, x_nab = feats[: len(rows)], feats[len(rows) :]
    y = np.array([r[2] for r in rows])
    y_nab = np.array([s for s, _ in nab])
    zs_text = embed.embed_texts(BACKBONE, _prompts())

    gate = None
    inc_train, test = gate_split(ids, incumbent_max)
    if current is not None and len(test):
        cand_train = np.setdiff1d(np.arange(len(rows)), test)
        gate = {
            "n": len(test),
            "incumbent": _score(_fit(x[inc_train], y[inc_train], x_nab, y_nab),
                                x[test], y[test], zs_text),
            "candidate": _score(_fit(x[cand_train], y[cand_train], x_nab, y_nab),
                                x[test], y[test], zs_text),
        }  # fmt: skip
        if not passes(gate["candidate"], gate["incumbent"]) and not force:
            c, i = gate["candidate"], gate["incumbent"]
            reason = (
                f"rejected: top-1 {c['top1']:.1%} vs {i['top1']:.1%}, "
                f"top-3 {c['top3']:.1%} vs {i['top3']:.1%} on {len(test)} gate crops"
            )
            result = Retrain(False, reason, current_head, new, gate)
            _record(store, result, len(rows), int(ids.max()))
            log.warning("retrain %s", reason)
            return result

    # The plain time split (oldest 80% -> newest 20% of every label), for the record.
    cut = int(len(rows) * (1 - TEST_FRACTION))
    heldout = _score(_fit(x[:cut], y[:cut], x_nab, y_nab), x[cut:], y[cut:], zs_text)

    head = _fit(x, y, x_nab, y_nab)
    now = dt.datetime.now()
    name = f"head-{now:%Y%m%d-%H%M%S}.joblib"
    models.mkdir(parents=True, exist_ok=True)
    joblib.dump({"head": head, "zs_text": zs_text, "backbone": BACKBONE}, models / name)
    meta = {
        "head": name,
        "trained_at": now.isoformat(timespec="seconds"),
        "labels": len(rows),
        "new_labels": new,
        "max_label_id": int(ids.max()) if len(ids) else 0,
        "nabirds": len(nab),
        "heldout": heldout,
        "gate": gate,
    }
    tmp = pointer.with_suffix(".tmp")
    tmp.write_text(json.dumps(meta, indent=2))
    tmp.replace(pointer)  # atomic: the live Classifier never reads half a file
    reason = "accepted" if gate else "accepted (no current head to compare with)"
    if force and gate and not passes(gate["candidate"], gate["incumbent"]):
        reason = "forced past a failing gate"
    result = Retrain(True, reason, name, new, gate)
    _record(store, result, len(rows), meta["max_label_id"])
    _prune(models, keep=name)
    log.info("retrain %s: %s on %d labels (%d new), held-out top-1 %.1f%%",
             reason, name, len(rows), new, 100 * heldout["top1"])  # fmt: skip
    return result


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
