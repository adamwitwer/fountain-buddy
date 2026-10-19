"""Phase 5: the gated retrain and the weekly report, on synthetic features (no BioCLIP)."""

import json
from contextlib import closing

import numpy as np
import pytest

from fountain_buddy import bakeoff, classifier, db, embed, species

DIM = 32
BIRDS = ["Northern Cardinal", "House Finch", "Tufted Titmouse"]


@pytest.fixture
def world(tmp_path, monkeypatch):
    """A store whose crop 'paths' embed to a per-species cluster, given by the name."""
    rng = np.random.default_rng(0)
    centers = {s: rng.normal(size=DIM) for s in BIRDS}

    def fake_paths(name, paths, cache_file):
        out = []
        for p in paths:
            truth, seed = p.stem.rsplit("-", 1)
            v = centers[truth.replace("_", " ")] + 0.6 * np.random.default_rng(int(seed)).normal(
                size=DIM
            )
            out.append(v / np.linalg.norm(v))
        return np.array(out)

    text = rng.normal(size=(len(species.SPECIES), DIM))
    monkeypatch.setattr(embed, "embed_paths", fake_paths)
    monkeypatch.setattr(embed, "embed_texts", lambda name, prompts: text / 1e3)
    monkeypatch.setattr(bakeoff, "nabirds_rows", lambda data_dir: [])
    store = tmp_path / "fb.db"
    db.init(store)
    return store, tmp_path


_n = [0]


def add(store, truth, label=None, n=1, day="2026-10-19"):
    """n visits whose crop looks like `truth`, labeled `label` (default: the truth)."""
    with closing(db.connect(store)) as conn:
        for _ in range(n):
            _n[0] += 1
            vid = conn.execute(
                "INSERT INTO visits (taken_at, camera, source) VALUES (?, 'tray', 'live')",
                (f"{day}T08:{_n[0] // 60 % 60:02d}:{_n[0] % 60:02d}",),
            ).lastrowid
            conn.execute(
                "INSERT INTO crops (visit_id, method, x1, y1, x2, y2, path) "
                "VALUES (?, 'det', 0, 0, 1, 1, ?)",
                (vid, f"crops/{truth.replace(' ', '_')}-{_n[0]}.jpg"),
            )
            conn.execute(
                "INSERT INTO labels (visit_id, label, source, labeled_at) "
                "VALUES (?, ?, 'discord', '2026-10-19T09:00:00')",
                (vid, label or truth),
            )
        conn.commit()


def head_json(data_dir):
    return json.loads((data_dir / "models" / "head.json").read_text())


def test_gate_split_holds_out_the_newest_known_rows():
    train, test = classifier.gate_split(np.array([5, 1, 2, 9, 3, 4, 6, 7, 8, 10, 11]), 8)
    # rows with label id <= 8, in time order: indices 0,1,2,4,5,6,7,8 -> newest 20%: 7, 8
    assert list(test) == [7, 8] and list(train) == [0, 1, 2, 4, 5, 6]


def test_passes_within_tolerance():
    inc = {"top1": 0.80, "top3": 0.95}
    assert classifier.passes({"top1": 0.797, "top3": 0.95}, inc)
    assert not classifier.passes({"top1": 0.79, "top3": 0.99}, inc)
    assert not classifier.passes({"top1": 0.85, "top3": 0.94}, inc)


def test_retrain_learns_good_answers_and_rejects_bad_ones(world):
    store, data_dir = world
    for s in BIRDS:
        add(store, s, n=40, day="2026-10-01")

    first = classifier.retrain(store, data_dir)
    assert first.accepted and first.gate is None and first.new_labels == 120
    assert head_json(data_dir)["max_label_id"] == 120

    assert classifier.retrain(store, data_dir).reason == "no new labels"

    for s in BIRDS:
        add(store, s, n=5, day="2026-10-20")
    good = classifier.retrain(store, data_dir)
    assert good.accepted and good.new_labels == 15 and good.gate["n"] == 24
    assert head_json(data_dir)["head"] == good.head

    # A flood of wrong answers: cardinals labeled House Finch.
    add(store, "Northern Cardinal", "House Finch", n=150, day="2026-10-21")
    bad = classifier.retrain(store, data_dir)
    assert not bad.accepted and bad.reason.startswith("rejected")
    assert head_json(data_dir)["head"] == good.head  # unchanged
    with closing(db.connect(store)) as conn:
        rows = conn.execute("SELECT accepted, new_labels FROM trainings ORDER BY id").fetchall()
    assert [tuple(r) for r in rows] == [(1, 120), (1, 15), (0, 150)]

    forced = classifier.retrain(store, data_dir, force=True)
    assert forced.accepted and forced.reason == "forced past a failing gate"


def test_retrain_ignores_test_posts_and_unknown_species(world):
    store, data_dir = world
    for s in BIRDS:
        add(store, s, n=20, day="2026-10-01")
    classifier.retrain(store, data_dir)
    add(store, "House Finch", "Painted Bunting", n=3)  # typed, not in species.LABELS
    with closing(db.connect(store)) as conn:
        conn.execute("UPDATE visits SET source = 'test' WHERE id = (SELECT MAX(id) FROM visits)")
        conn.commit()
    assert classifier.retrain(store, data_dir).reason == "no new labels"


def test_old_heads_are_pruned(world):
    store, data_dir = world
    models = data_dir / "models"
    models.mkdir()
    for i in range(15):
        (models / f"head-20260101-0000{i:02d}.joblib").write_text("")
    for s in BIRDS:
        add(store, s, n=20)
    result = classifier.retrain(store, data_dir)
    heads = sorted(p.name for p in models.glob("head-*.joblib"))
    assert len(heads) == classifier.KEEP_HEADS and result.head in heads


def _post(store, truth, guess, day):
    """A live post whose model ranked `guess` first and was answered `truth`."""
    with closing(db.connect(store)) as conn:
        vid = conn.execute(
            "INSERT INTO visits (taken_at, camera, source) VALUES (?, 'tray', 'live')",
            (f"{day}T09:00:00",),
        ).lastrowid
        ranked = [guess] + [s for s in BIRDS + [species.SKIP] if s != guess]
        conn.execute(
            "INSERT INTO predictions (visit_id, model, label, top_k, predicted_at) "
            "VALUES (?, 'h', ?, ?, ?)",
            (vid, guess, json.dumps([[s, 0.1] for s in ranked]), day),
        )
        conn.execute("INSERT INTO posts VALUES (?, ?, 1, ?)", (vid + 10_000, vid, day))
        if truth:
            conn.execute(
                "INSERT INTO labels (visit_id, label, source, labeled_at) "
                "VALUES (?, ?, 'discord', ?)",
                (vid, truth, day),
            )
        conn.commit()


def test_weekly_report(tmp_path):
    import datetime as dt

    from fountain_buddy import report

    store = tmp_path / "fb.db"
    db.init(store)
    for _ in range(3):
        _post(store, "Northern Cardinal", "Northern Cardinal", "2026-10-15")
    _post(store, "House Finch", "Northern Cardinal", "2026-10-16")
    _post(store, "American Goldfinch", "Northern Cardinal", "2026-10-17")  # not on a button
    _post(store, species.SKIP, species.SKIP, "2026-10-18")
    _post(store, None, "House Finch", "2026-10-18")  # unanswered
    _post(store, "House Finch", "House Finch", "2026-10-09")  # the week before
    with closing(db.connect(store)) as conn:
        conn.executemany(
            "INSERT INTO trainings (trained_at, accepted, labels, new_labels, max_label_id, "
            "reason) VALUES (?, ?, 10, 1, 1, 'x')",
            [("2026-10-16T10:00:00", 1), ("2026-10-17T10:00:00", 0)],
        )
        conn.commit()
    text = report.weekly_text(store, tmp_path, dt.date(2026, 10, 18))
    assert "7 photos, 6 answered" in text
    assert "Birds: 5. First guess right on 3 (60%); your answer was a button on 4 (80%)" in text
    assert "Last week: 100% first guess" in text
    assert "Northern Cardinal 3/3" in text and "American Goldfinch 0/1" in text
    assert "House Finch called Northern Cardinal" in text
    assert "Skip: 1" in text
    assert "retrained 1×, 1 rejected by the check" in text
    assert report.weekly_text(store, tmp_path, dt.date(2026, 11, 30)) is None
