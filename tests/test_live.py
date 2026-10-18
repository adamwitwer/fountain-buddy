"""The live path without hardware: fake detector and classifier, no Discord connection."""

import asyncio
import datetime as dt
from contextlib import closing

import numpy as np

from fountain_buddy import bot, db, species
from fountain_buddy.classifier import blend_zero_shot
from fountain_buddy.detect import Detection
from fountain_buddy.pipeline import Pipeline
from fountain_buddy.service import summary_text

RANKED = [
    ("Northern Cardinal", 0.81),
    ("House Finch", 0.1),
    ("Skip", 0.05),
    ("Mourning Dove", 0.04),
]


class FakeDetector:
    name = "fake@1280"

    def __init__(self, per_frame):
        self.per_frame = iter(per_frame)

    def birds(self, frame):
        return next(self.per_frame)


class FakeClassifier:
    version = "head-test.joblib"

    def predict(self, crop):
        assert crop.shape[:2] == (100, 200)
        return RANKED


def _frames(n=3):
    return [np.full((720, 1280, 3), 90, np.uint8) for _ in range(n)]


def test_pipeline_records_the_most_confident_bird(tmp_path):
    store = tmp_path / "fb.db"
    det = FakeDetector([[], [Detection(100, 100, 300, 200, 0.9)], [Detection(0, 0, 50, 50, 0.4)]])
    pipe = Pipeline(store, tmp_path, det, FakeClassifier())
    when = dt.datetime(2026, 10, 19, 8, 15, 2)
    sighting = pipe.process(_frames(), now=when)

    assert sighting.ranked == RANKED and sighting.det_conf == 0.9
    assert sighting.preview_path.exists()
    with closing(db.connect(store)) as conn:
        visit = conn.execute("SELECT * FROM visits").fetchone()
        crop = conn.execute("SELECT * FROM crops").fetchone()
        pred = conn.execute("SELECT * FROM predictions").fetchone()
        assert conn.execute("SELECT COUNT(*) FROM labels").fetchone()[0] == 0  # never a label
    assert visit["source"] == "live" and visit["frame_marked"] == 0
    assert (tmp_path / visit["image_path"]).exists()
    assert (crop["x1"], crop["y1"], crop["x2"], crop["y2"]) == (100, 100, 300, 200)
    assert crop["method"] == "fake@1280" and (tmp_path / crop["path"]).exists()
    assert pred["label"] == "Northern Cardinal" and pred["model"] == "head-test.joblib"


def test_pipeline_keeps_a_reject_frame_when_no_bird(tmp_path):
    pipe = Pipeline(tmp_path / "fb.db", tmp_path, FakeDetector([[], []]), FakeClassifier())
    assert pipe.process(_frames(2), now=dt.datetime(2026, 10, 19, 8, 0, 0)) is None
    assert (tmp_path / "rejects" / "2026-10-19" / "080000.jpg").exists()
    pipe.prune_rejects(today=dt.date(2026, 10, 30))
    assert not (tmp_path / "rejects" / "2026-10-19").exists()


def test_parse_reply():
    assert bot.parse_reply("northern cardinal") == "Northern Cardinal"
    assert bot.parse_reply("blurry, skip") == species.SKIP
    assert bot.parse_reply("too blur") == species.SKIP
    assert bot.parse_reply("Pine Siskin") == "Pine Siskin"  # unknown species kept as typed
    assert bot.parse_reply("   ") is None


def test_blend_keeps_non_species_mass():
    classes = ["Northern Cardinal", "House Finch", "Skip"]
    proba = np.array([[0.5, 0.2, 0.3]])
    zs = np.zeros((1, len(species.SPECIES)))
    zs[0, species.SPECIES.index("House Finch")] = 0.9
    zs[0, species.SPECIES.index("Northern Cardinal")] = 0.1
    out = blend_zero_shot(proba, classes, zs)
    assert abs(out.sum() - 1) < 1e-9 and abs(out[0, 2] - 0.3) < 1e-9
    assert out[0, 1] > proba[0, 1]  # zero-shot pulled toward House Finch


def _visit(store, label=None):
    pipe = Pipeline(store, store.parent, FakeDetector([[Detection(100, 100, 300, 200, 0.9)]]),
                    FakeClassifier())  # fmt: skip
    s = pipe.process(_frames(1), now=dt.datetime(2026, 10, 19, 14, 5, 9))
    if label:
        bot.add_label(store, s.visit_id, label, "Adam")
    return s.visit_id


def test_render_open_and_labeled(tmp_path):
    store = tmp_path / "fb.db"
    visit_id = _visit(store)

    async def go():
        embed, view = bot.render(bot.visit_state(store, visit_id))
        ids = [item.custom_id for item in view.children]
        assert embed.title.startswith("Northern Cardinal?")
        # Top species become buttons (Skip is not among them), then dropdown, Skip, Not a bird.
        assert ids == [
            f"fb:l:{visit_id}:Northern Cardinal", f"fb:l:{visit_id}:House Finch",
            f"fb:l:{visit_id}:Mourning Dove", f"fb:o:{visit_id}",
            f"fb:l:{visit_id}:Skip", f"fb:l:{visit_id}:Not a bird",
        ]  # fmt: skip
        assert all(len(i) <= 100 for i in ids)

        bot.add_label(store, visit_id, "House Finch", "Adam")
        embed, view = bot.render(bot.visit_state(store, visit_id))
        assert embed.title == "✅ House Finch"
        assert (
            "Labeled by Adam" in embed.description
            and "guessed Northern Cardinal" in embed.description
        )
        assert [i.custom_id for i in view.children] == [f"fb:c:{visit_id}"]

    asyncio.run(go())


def test_dropdown_fits_discord():
    assert len(bot.DROPDOWN) <= 25


def test_summary(tmp_path):
    store = tmp_path / "fb.db"
    ids = [_visit(store, "Northern Cardinal"), _visit(store, "House Finch"), _visit(store)]
    with closing(db.connect(store)) as conn:
        for i, visit_id in enumerate(ids):
            conn.execute(
                "INSERT INTO posts VALUES (?, ?, 1, '2026-10-19T14:05:10')", (1000 + i, visit_id)
            )
        conn.commit()
    text = summary_text(store, dt.date(2026, 10, 19))
    assert "3 photos, 2 answered" in text
    assert "Northern Cardinal: 1" in text and "agreed with you on 1/2" in text
    assert "1 still unanswered" in text
    assert summary_text(store, dt.date(2026, 10, 20)) is None


def test_camera_connect_times_out_instead_of_hanging(monkeypatch):
    import pytest

    from fountain_buddy import camera

    monkeypatch.setattr(camera, "CONNECT_TIMEOUT_SECONDS", 0.05)

    async def go():
        cam = camera.Camera("192.0.2.1", "user", "pass")  # TEST-NET-1: never reachable

        async def hang():
            await asyncio.sleep(10)

        cam.host.get_host_data = hang
        with pytest.raises(TimeoutError):
            await cam.connect()

    asyncio.run(go())
