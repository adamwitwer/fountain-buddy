"""The live path without hardware: fake detector and classifier, no Discord connection."""

import asyncio
import datetime as dt
from contextlib import closing

import numpy as np
import pytest

from fountain_buddy import bot, db, species
from fountain_buddy.classifier import blend_zero_shot
from fountain_buddy.detect import Detection
from fountain_buddy.pipeline import Pipeline, Region
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
    pipe.prune_rejects(today=dt.date(2026, 10, 21))
    assert (tmp_path / "rejects" / "2026-10-19").exists()  # two days back: kept
    pipe.prune_rejects(today=dt.date(2026, 10, 22))
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


def _visit(store, label=None, minute=5):
    pipe = Pipeline(store, store.parent, FakeDetector([[Detection(100, 100, 300, 200, 0.9)]]),
                    FakeClassifier())  # fmt: skip
    s = pipe.process(_frames(1), now=dt.datetime(2026, 10, 19, 14, minute, 9))
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
    ids = [_visit(store, "Northern Cardinal", 5), _visit(store, "House Finch", 15),
           _visit(store, None, 25)]  # fmt: skip
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


class Sure:
    """A classifier that is sure of one label."""

    version = "head-test.joblib"

    def __init__(self, label="Tufted Titmouse", p=0.98):
        self.label, self.p = label, p

    def predict(self, crop):
        return [(self.label, self.p), ("Skip", 0.01), ("House Finch", 0.01)]


class Rolls:
    """A stand-in for random.Random: 0.99 never picks a spot check, 0.0 always does."""

    def __init__(self, value):
        self.value = value

    def random(self):
        return self.value


BIRD = Detection(100, 100, 300, 200, 0.6)
T0 = dt.datetime(2026, 10, 29, 9, 0, 0)


def _pipe(tmp_path, classifier, n=1, roll=0.99, source="live"):
    pipe = Pipeline(tmp_path / "fb.db", tmp_path, FakeDetector([[BIRD]] * n), classifier,
                    source=source)  # fmt: skip
    pipe.rng = Rolls(roll)
    return pipe


def test_a_repeat_of_the_same_guess_is_held_back(tmp_path):
    pipe = _pipe(tmp_path, Sure(), n=4)
    assert pipe.process(_frames(1), now=T0) is not None
    later = T0 + dt.timedelta(minutes=4, seconds=59)
    assert pipe.process(_frames(1), now=later) is None
    assert (tmp_path / "rejects" / "2026-10-29" / "090459-repeat.jpg").exists()
    # The window runs from the last post, not the last burst.
    assert pipe.process(_frames(1), now=T0 + dt.timedelta(minutes=5)) is not None


def test_a_different_guess_still_posts_during_a_run(tmp_path):
    _pipe(tmp_path, Sure("Tufted Titmouse")).process(_frames(1), now=T0)
    cardinal = _pipe(tmp_path, Sure("Northern Cardinal"))
    assert cardinal.process(_frames(1), now=T0 + dt.timedelta(minutes=1)) is not None


def test_a_sure_guess_is_auto_accepted_but_never_a_label(tmp_path):
    store = tmp_path / "fb.db"
    sighting = _pipe(tmp_path, Sure(p=0.97)).process(_frames(1), now=T0)
    assert sighting.auto_accepted
    with closing(db.connect(store)) as conn:
        assert conn.execute("SELECT spot_check FROM auto_accepts").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM labels").fetchone()[0] == 0

    async def go():
        embed, view = bot.render(bot.visit_state(store, sighting.visit_id))
        assert embed.title.startswith("☑️ Tufted Titmouse") and "not trained on" in embed.description
        assert [i.custom_id for i in view.children] == [f"fb:c:{sighting.visit_id}"]
        bot.add_label(store, sighting.visit_id, "Carolina Wren", "Adam")  # Change, then a tap
        embed, _ = bot.render(bot.visit_state(store, sighting.visit_id))
        assert embed.title == "✅ Carolina Wren"

    asyncio.run(go())


def test_a_spot_check_asks_as_usual(tmp_path):
    store = tmp_path / "fb.db"
    sighting = _pipe(tmp_path, Sure(), roll=0.0).process(_frames(1), now=T0)
    assert not sighting.auto_accepted
    with closing(db.connect(store)) as conn:
        assert conn.execute("SELECT spot_check FROM auto_accepts").fetchone()[0] == 1

    async def go():
        embed, view = bot.render(bot.visit_state(store, sighting.visit_id))
        assert embed.title.startswith("Tufted Titmouse?") and len(view.children) > 1
        assert "🔍 Spot check" in embed.description

    asyncio.run(go())


@pytest.mark.parametrize(
    "classifier, source",
    [(Sure(p=0.96), "live"), (Sure("Skip", 0.99), "live"),
     (Sure("Not a bird", 0.99), "live"), (Sure(), "test")],
)  # fmt: skip
def test_what_is_never_auto_accepted(tmp_path, classifier, source):
    sighting = _pipe(tmp_path, classifier, source=source).process(_frames(1), now=T0)
    assert sighting is not None and not sighting.auto_accepted
    with closing(db.connect(tmp_path / "fb.db")) as conn:
        assert conn.execute("SELECT COUNT(*) FROM auto_accepts").fetchone()[0] == 0


def test_summary_and_report_count_auto_accepts_apart(tmp_path):
    from fountain_buddy import report

    store = tmp_path / "fb.db"
    auto = _pipe(tmp_path, Sure()).process(_frames(1), now=T0)
    check = _pipe(tmp_path, Sure("Northern Cardinal"), roll=0.0).process(_frames(1), now=T0)
    changed = _pipe(tmp_path, Sure("House Finch")).process(_frames(1), now=T0)
    bot.add_label(store, check.visit_id, "Northern Cardinal", "Adam")
    bot.add_label(store, changed.visit_id, "Purple Finch", "Adam")
    with closing(db.connect(store)) as conn:
        for i, s in enumerate((auto, check, changed)):
            conn.execute("INSERT INTO posts VALUES (?, ?, 1, ?)", (i, s.visit_id, T0.isoformat()))
        conn.commit()

    text = summary_text(store, T0.date())
    assert "3 photos, 2 answered, 1 auto-accepted" in text and "unanswered" not in text
    assert "Tufted Titmouse: 1" in text
    assert "agreed with you on 1/1" in text  # the changed auto-accept doesn't count against
    weekly = report.weekly_text(store, tmp_path / "models", T0.date())
    assert "Auto-accepted: 2 (not asked), 1 changed by you" in weekly
    assert "Spot checks: right on 1/1 (100%)" in weekly
    assert "Birds: 1." in weekly


def test_percentages_round_down_so_97_means_auto_accepted(tmp_path):
    store = tmp_path / "fb.db"
    sighting = _pipe(tmp_path, Sure(p=0.96996)).process(_frames(1), now=T0)
    assert not sighting.auto_accepted  # top_k stores 0.97; the threshold saw 0.96996

    async def go():
        embed, _ = bot.render(bot.visit_state(store, sighting.visit_id))
        assert embed.title == "Tufted Titmouse?  (96%)"
        assert "Spot check" not in embed.description

    asyncio.run(go())
    assert bot._pct(0.97) == "97%" and bot._pct(0.9999) == "99%" and bot._pct(0.05) == "5%"


class SeesShapes:
    """A detector that finds one bird at a fixed spot in whatever it's shown."""

    name = "fake@1280"

    def __init__(self):
        self.shapes = []

    def birds(self, frame):
        self.shapes.append(frame.shape[:2])
        return [Detection(10, 20, 110, 70, 0.8)]


REGION = Region((0.25, 0.5, 0.75, 1.0), "2026-11-07T14:00:00")


def test_the_detector_sees_only_the_region_and_boxes_stay_in_frame_pixels(tmp_path):
    store, det = tmp_path / "fb.db", SeesShapes()
    pipe = Pipeline(store, tmp_path, det, Sure(), region=REGION)
    pipe.rng = Rolls(0.99)
    sighting = pipe.process(_frames(1), now=dt.datetime(2026, 11, 7, 15, 0, 0))
    assert det.shapes == [(360, 640)]
    with closing(db.connect(store)) as conn:
        crop = conn.execute("SELECT x1, y1, x2, y2 FROM crops").fetchone()
    assert tuple(crop) == (330, 380, 430, 430)
    assert sighting is not None and pipe.region_text() == "cropped to x 25-75%, y 50-100%"


def test_a_camera_move_after_the_region_was_set_switches_it_off(tmp_path):
    store = tmp_path / "fb.db"
    db.init(store)
    with closing(db.connect(store)) as conn:
        conn.execute("INSERT INTO camera_moves (camera, moved_at) VALUES ('tray', ?)",
                     ("2026-11-07T13:39:30",))  # fmt: skip
        conn.commit()
    det = SeesShapes()
    pipe = Pipeline(store, tmp_path, det, Sure(), region=REGION)
    pipe.process(_frames(1), now=dt.datetime(2026, 11, 7, 15, 0, 0))
    assert det.shapes == [(360, 640)]  # the move came before the region: it applies
    with closing(db.connect(store)) as conn:
        conn.execute("INSERT INTO camera_moves (camera, moved_at) VALUES ('tray', ?)",
                     ("2026-11-08T09:00:00",))  # fmt: skip
        conn.commit()
    pipe.process(_frames(1), now=dt.datetime(2026, 11, 8, 10, 0, 0))
    assert det.shapes[-1] == (720, 1280)
    assert "from before the camera moved" in pipe.region_text(dt.datetime(2026, 11, 8, 10, 0, 0))


@pytest.mark.parametrize(
    "entry",
    [{"box": [0.5, 0.1, 0.4, 0.9], "set_at": "2026-11-07T14:00:00"},
     {"box": [0.1, 0.1, 1.2, 0.9], "set_at": "2026-11-07T14:00:00"},
     {"box": [0.1, 0.1, 0.9, 0.9]}],
)  # fmt: skip
def test_a_malformed_region_is_refused(entry):
    with pytest.raises((ValueError, KeyError)):
        Region.from_config({"region": entry})
    assert Region.from_config({}) is None


def test_crop_command_writes_and_clears_the_region(tmp_path, monkeypatch, capsys):
    import json

    from fountain_buddy import __main__ as cli
    from fountain_buddy.config import Settings

    cfg = Settings(camera_host="192.0.2.1", camera_username="u", data_dir=tmp_path)
    monkeypatch.setattr(cli, "settings", lambda: cfg)
    assert cli.main(["crop", "25", "15", "60", "70"]) == 0
    config = json.loads((cfg.models_dir / "detector.json").read_text())
    assert config["weights"] == "yolo26m.pt" and config["region"]["box"] == [0.25, 0.15, 0.6, 0.7]
    assert Region.from_config(config).text() == "x 25-60%, y 15-70%"
    assert "Restart the service" in capsys.readouterr().out

    assert cli.main(["camera-moved", "--at", "2099-01-01T00:00"]) == 0
    assert "set for the old view" in capsys.readouterr().out
    assert cli.main(["crop", "--off"]) == 0
    assert "region" not in json.loads((cfg.models_dir / "detector.json").read_text())
    assert cli.main(["crop", "60", "15", "25", "70"]) == 2
