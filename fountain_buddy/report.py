"""The weekly agreement report: how often the model's guess matched Adam's answer, and
what the learning loop did. Posted to Discord on Sundays; `fountain-buddy report` prints it.

Every prediction was made before its answer existed, so agreement here is an honest
out-of-sample score for the scene the camera sees now.
"""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from contextlib import closing
from pathlib import Path

from fountain_buddy import db, species


def answered(store: Path, start: dt.date, end: dt.date) -> list[dict]:
    """Answered live posts taken in [start, end): label, first guess, button labels."""
    with closing(db.connect(store)) as conn:
        rows = conn.execute(
            "SELECT l.label, p.top_k FROM visits v "
            "JOIN posts ON posts.visit_id = v.id "
            "JOIN current_labels l ON l.visit_id = v.id "
            "JOIN predictions p "
            "ON p.id = (SELECT MAX(id) FROM predictions WHERE visit_id = v.id) "
            "WHERE v.source = 'live' AND v.taken_at >= ? AND v.taken_at < ?",
            (start.isoformat(), end.isoformat()),
        ).fetchall()
    out = []
    for r in rows:
        ranked = [label for label, _ in json.loads(r["top_k"])]
        buttons = [label for label in ranked if label in species.SPECIES][:3]
        out.append({"label": r["label"], "guess": ranked[0], "buttons": buttons})
    return out


def _agreement(rows: list[dict]) -> tuple[int, int, int]:
    """(birds, first guess right, answer on a button) over answers that are species."""
    birds = [r for r in rows if r["label"] in species.SPECIES]
    return (
        len(birds),
        sum(r["guess"] == r["label"] for r in birds),
        sum(r["label"] in r["buttons"] for r in birds),
    )


def weekly_text(store: Path, models_dir: Path, last_day: dt.date) -> str | None:
    """The report for the 7 days ending on last_day, or None if nothing was posted."""
    start, end = last_day - dt.timedelta(days=6), last_day + dt.timedelta(days=1)
    with closing(db.connect(store)) as conn:
        posted = conn.execute(
            "SELECT COUNT(*) FROM posts JOIN visits v ON v.id = posts.visit_id "
            "WHERE v.source = 'live' AND v.taken_at >= ? AND v.taken_at < ?",
            (start.isoformat(), end.isoformat()),
        ).fetchone()[0]
        trainings = conn.execute(
            "SELECT accepted FROM trainings WHERE trained_at >= ? AND trained_at < ?",
            (start.isoformat(), end.isoformat()),
        ).fetchall()
        tray_labels = conn.execute(
            "SELECT COUNT(*) FROM current_labels l JOIN visits v ON v.id = l.visit_id "
            "WHERE v.source = 'live'"
        ).fetchone()[0]
    if not posted:
        return None
    rows = answered(store, start, end)
    birds, right, on_button = _agreement(rows)

    lines = [
        f"📊 **Week at the tray** ({start:%b %-d}–{last_day:%b %-d}): "
        f"{posted} photos, {len(rows)} answered"
    ]
    if birds:
        line = (
            f"Birds: {birds}. First guess right on {right} ({right / birds:.0%}); "
            f"your answer was a button on {on_button} ({on_button / birds:.0%})."
        )
        prev = _agreement(answered(store, start - dt.timedelta(days=7), start))
        if prev[0]:
            line += f" Last week: {prev[1] / prev[0]:.0%} first guess."
        lines.append(line)

        seen = Counter(r["label"] for r in rows if r["label"] in species.SPECIES)
        hits = Counter(r["label"] for r in rows if r["label"] == r["guess"])
        lines.append(
            " · ".join(f"{name} {hits[name]}/{n}" for name, n in seen.most_common())
            + " (right/seen)"
        )
        mixups = Counter(
            (r["label"], r["guess"])
            for r in rows
            if r["label"] in species.SPECIES and r["guess"] != r["label"]
        )
        if mixups:
            lines.append(
                "Mix-ups: "
                + "; ".join(
                    f"{truth} called {guess}" + (f" ×{n}" if n > 1 else "")
                    for (truth, guess), n in mixups.most_common(3)
                )
            )
    others = Counter(r["label"] for r in rows if r["label"] not in species.SPECIES)
    if others:
        lines.append(", ".join(f"{label}: {n}" for label, n in others.most_common()))

    pointer = models_dir / "head.json"
    head = json.loads(pointer.read_text()) if pointer.exists() else None
    rejected = sum(not r["accepted"] for r in trainings)
    learning = f"Learning: retrained {len(trainings) - rejected}×"
    if rejected:
        learning += f", {rejected} rejected by the check"
    if head:
        learning += f". Now trained on {head['labels']:,} answers ({tray_labels} from the tray)."
    lines.append(learning)
    return "\n".join(lines)
