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


def _frames(n=3, colour=(60, 110, 150)):
    """Daylight frames (BGR, saturated); colour=(90, 90, 90) is an infrared night frame."""
    return [np.full((720, 1280, 3), colour, np.uint8) for _ in range(n)]


NIGHT = (90, 90, 90)


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


def test_status_text(tmp_path):
    import time

    from fountain_buddy.config import Settings
    from fountain_buddy.service import status_text

    cfg = Settings(camera_host="192.0.2.1", camera_username="u", data_dir=tmp_path)
    db.init(cfg.db_path)
    now = time.time()
    text = status_text(cfg, now - 7200, now - 30, "yolo26m@1280", "head-x.joblib", now=now)
    assert "Running for 2.0 h" in text and "last OK 30 s ago ✅" in text
    assert "Last bird: none yet" in text and "0 birds posted" in text
    assert "0 night visitors ignored" in text
    stale = status_text(cfg, now - 7200, now - 3600, "d", "h", now=now)
    assert "last OK 60 min ago ⚠️" in stale
    assert "never reached since start ⚠️" in status_text(cfg, now, 0.0, "d", "h", now=now)


class SaysClassifier:
    version = "head-test.joblib"

    def __init__(self, label):
        self.label = label

    def predict(self, crop):
        return [(self.label, 0.97), ("Skip", 0.02), ("House Finch", 0.01)]


def _not_a_bird_at(store, box, day="2026-10-19T12:03:31"):
    db.init(store)
    with closing(db.connect(store)) as conn:
        vid = conn.execute(
            "INSERT INTO visits (taken_at, camera, source) VALUES (?, 'tray', 'live')", (day,)
        ).lastrowid
        conn.execute(
            "INSERT INTO crops (visit_id, method, x1, y1, x2, y2, path) "
            "VALUES (?, 'd', ?, ?, ?, ?, 'c.jpg')",
            (vid, *box),
        )
        conn.execute(
            "INSERT INTO labels (visit_id, label, source, labeled_at) "
            "VALUES (?, 'Not a bird', 'discord', ?)",
            (vid, day),
        )
        conn.commit()


BRACKET = (1728, 1580, 2138, 1813)  # the box from 2026-10-19's dusk posts, at 4K
NEAR_BRACKET = Detection(173, 158, 214, 181, 0.38)  # the same spot on a 1280-wide frame


def test_known_not_a_bird_spot_is_ignored(tmp_path):
    store = tmp_path / "fb.db"
    _not_a_bird_at(store, tuple(v // 10 for v in BRACKET))
    pipe = Pipeline(
        store, tmp_path, FakeDetector([[NEAR_BRACKET]] * 2), SaysClassifier("Not a bird")
    )
    when = dt.datetime(2026, 10, 19, 18, 40, 2)
    assert pipe.process(_frames(2), now=when) is None
    assert (tmp_path / "rejects" / "2026-10-19" / "184002-spot.jpg").exists()


def test_a_bird_on_a_known_spot_still_posts(tmp_path):
    store = tmp_path / "fb.db"
    _not_a_bird_at(store, tuple(v // 10 for v in BRACKET))
    pipe = Pipeline(
        store, tmp_path, FakeDetector([[NEAR_BRACKET]]), SaysClassifier("Northern Cardinal")
    )
    assert pipe.process(_frames(1)) is not None


def test_a_bird_elsewhere_beats_a_more_confident_spot(tmp_path):
    store = tmp_path / "fb.db"
    _not_a_bird_at(store, tuple(v // 10 for v in BRACKET))
    bird = Detection(500, 100, 600, 180, 0.15)
    pipe = Pipeline(
        store, tmp_path, FakeDetector([[NEAR_BRACKET, bird]]), SaysClassifier("House Finch")
    )
    sighting = pipe.process(_frames(1))
    assert sighting.det_conf == 0.15


def test_old_not_a_bird_answers_expire(tmp_path):
    store = tmp_path / "fb.db"
    _not_a_bird_at(store, tuple(v // 10 for v in BRACKET), day="2026-08-01T12:00:00")
    pipe = Pipeline(store, tmp_path, FakeDetector([[NEAR_BRACKET]]), SaysClassifier("Not a bird"))
    assert pipe.process(_frames(1), now=dt.datetime(2026, 10, 19, 18, 0, 0)) is not None


def test_ivy_swaying_off_its_first_box_still_counts_as_the_spot(tmp_path):
    store = tmp_path / "fb.db"
    _not_a_bird_at(store, (61, 166, 101, 204))  # 2026-10-20's ivy sprig, 1/10 scale
    swayed = Detection(46, 172, 93, 204, 0.18)  # IoU 0.51 with the answered box
    pipe = Pipeline(store, tmp_path, FakeDetector([[swayed]]), SaysClassifier("Not a bird"))
    assert pipe.process(_frames(1), now=dt.datetime(2026, 10, 20, 10, 39, 53)) is None


def test_infrared_burst_that_is_not_a_bird_is_ignored(tmp_path):
    store = tmp_path / "fb.db"
    mouse = Detection(150, 130, 210, 180, 0.42)
    pipe = Pipeline(store, tmp_path, FakeDetector([[mouse]]), SaysClassifier("Not a bird"))
    when = dt.datetime(2026, 10, 20, 3, 23, 30)
    assert pipe.process(_frames(1, NIGHT), now=when) is None
    assert (tmp_path / "rejects" / "2026-10-20" / "032330-night.jpg").exists()


def test_infrared_bird_still_posts(tmp_path):
    store = tmp_path / "fb.db"
    wren = Detection(200, 20, 285, 63, 0.54)  # 07:35, camera still in infrared
    pipe = Pipeline(store, tmp_path, FakeDetector([[wren]]), SaysClassifier("Carolina Wren"))
    assert pipe.process(_frames(1, NIGHT)) is not None


def test_daylight_not_a_bird_off_any_spot_still_posts(tmp_path):
    store = tmp_path / "fb.db"
    pipe = Pipeline(store, tmp_path, FakeDetector([[NEAR_BRACKET]]), SaysClassifier("Not a bird"))
    assert pipe.process(_frames(1)) is not None


def test_moving_the_camera_forgets_old_spots(tmp_path):
    store = tmp_path / "fb.db"
    _not_a_bird_at(store, tuple(v // 10 for v in BRACKET), day="2026-10-22T18:40:00")
    with closing(db.connect(store)) as conn:
        conn.execute(
            "INSERT INTO camera_moves (camera, moved_at) VALUES ('tray', '2026-10-23T10:47:00')"
        )
        conn.commit()
    before = Pipeline(store, tmp_path, FakeDetector([[NEAR_BRACKET]]), SaysClassifier("Not a bird"))
    assert before.process(_frames(1), now=dt.datetime(2026, 10, 23, 10, 0, 0)) is None
    after = Pipeline(store, tmp_path, FakeDetector([[NEAR_BRACKET]]), SaysClassifier("Not a bird"))
    assert after.process(_frames(1), now=dt.datetime(2026, 10, 23, 11, 0, 0)) is not None
