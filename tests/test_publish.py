"""The public page: what gets published, how visits group, and what the push may delete."""

import datetime as dt
from contextlib import closing

import pytest
from PIL import Image

from fountain_buddy import db, publish

NOW = dt.datetime(2026, 10, 22, 15, 0)


@pytest.fixture
def store(tmp_path):
    path = tmp_path / "fb.db"
    db.init(path)
    return path


def add(store, data_dir, when, label, guess=None, conf=0.5, camera="tray", source="live"):
    """A visit with a frame on disk, a crop, a guess and (if label) an answer."""
    rel = f"images/tray/{when:%Y-%m-%d}/{when:%H%M%S}.jpg"
    (data_dir / rel).parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (384, 216), (90, 120, 60)).save(data_dir / rel)
    with closing(db.connect(store)) as conn:
        vid = conn.execute(
            "INSERT INTO visits (taken_at, camera, image_path, source) VALUES (?, ?, ?, ?)",
            (when.isoformat(timespec="seconds"), camera, rel, source),
        ).lastrowid
        conn.execute(
            "INSERT INTO crops (visit_id, method, x1, y1, x2, y2, det_conf, path) "
            "VALUES (?, 'det', 0, 0, 1, 1, ?, 'c.jpg')",
            (vid, conf),
        )
        conn.execute(
            "INSERT INTO predictions (visit_id, model, label, confidence, top_k, predicted_at) "
            "VALUES (?, 'head', ?, 0.9, ?, ?)",
            (vid, guess or label or "Skip", f'[["{guess or label or "Skip"}", 0.9]]',
             when.isoformat()),
        )  # fmt: skip
        if label:
            conn.execute(
                "INSERT INTO labels (visit_id, label, source, labeled_at) "
                "VALUES (?, ?, 'discord', ?)",
                (vid, label, when.isoformat()),
            )
        conn.commit()
    return vid


def at(minutes_ago):
    return NOW - dt.timedelta(minutes=minutes_ago)


def test_only_answered_visitors_are_published(store, tmp_path):
    keep = add(store, tmp_path, at(10), "Carolina Wren")
    squirrel = add(store, tmp_path, at(20), "Squirrel")
    add(store, tmp_path, at(30), "Skip")
    add(store, tmp_path, at(40), "Not a bird")
    add(store, tmp_path, at(50), None, guess="Northern Cardinal")  # unanswered
    add(store, tmp_path, at(60), "Blue Jay", source="test")
    assert {p.visit_id for p in publish.load_photos(store)} == {keep, squirrel}


def test_relabel_uses_the_current_answer(store, tmp_path):
    vid = add(store, tmp_path, at(10), "House Sparrow")
    with closing(db.connect(store)) as conn:
        conn.execute(
            "INSERT INTO labels (visit_id, label, source, labeled_at) "
            "VALUES (?, 'Skip', 'discord', ?)",
            (vid, NOW.isoformat()),
        )
        conn.commit()
    assert publish.load_photos(store) == []


def test_visits_group_by_gap_per_visitor(store, tmp_path):
    for m in (100, 95, 90):  # one titmouse visit, 10 minutes long
        add(store, tmp_path, at(m), "Tufted Titmouse")
    add(store, tmp_path, at(93), "Northern Cardinal")  # arrives mid-visit
    add(store, tmp_path, at(70), "Tufted Titmouse")  # 20 min later: a new visit
    visits = publish.group_visits(publish.load_photos(store))
    assert [(v.label, len(v.photos)) for v in visits] == [
        ("Tufted Titmouse", 1),
        ("Tufted Titmouse", 3),
        ("Northern Cardinal", 1),
    ]


def test_best_photo_is_highest_detector_confidence(store, tmp_path):
    add(store, tmp_path, at(12), "Mourning Dove", conf=0.3)
    best = add(store, tmp_path, at(11), "Mourning Dove", conf=0.9)
    add(store, tmp_path, at(10), "Mourning Dove", conf=0.5)
    (visit,) = publish.group_visits(publish.load_photos(store))
    assert visit.best.visit_id == best


def test_build_keeps_recent_visits_and_each_visitors_best(store, tmp_path):
    old_best = add(store, tmp_path, NOW - dt.timedelta(days=20), "Carolina Wren", conf=0.95)
    old_other = add(store, tmp_path, NOW - dt.timedelta(days=15), "Carolina Wren", conf=0.2)
    recent = add(store, tmp_path, at(30), "Carolina Wren", guess="Skip", conf=0.4)
    out = tmp_path / "site"
    (out / "img").mkdir(parents=True)
    (out / "img" / "999.jpg").write_bytes(b"stale")

    publish.build(store, tmp_path, out, now=NOW)

    names = {p.name for p in (out / "img").iterdir()}
    assert names == {f"{v}{s}.jpg" for v in (old_best, recent) for s in ("", "-t")}
    assert f"{old_other}.jpg" not in names
    page = (out / "index.html").read_text()
    assert "Carolina Wren" in page
    assert "AI guessed a photo too blurry to use" in page
    assert "style=" not in page and "<script" not in page  # strict CSP on the host
    assert (out / "birds.css").exists() and (out / ".htaccess").exists()
    with Image.open(out / "img" / f"{recent}.jpg") as im:
        assert im.width == publish.FULL_WIDTH and not im.info.get("exif")


def test_page_escapes_and_handles_an_empty_tray(store, tmp_path):
    out = publish.build(store, tmp_path, tmp_path / "site", now=NOW)
    assert "Quiet tray" in (out / "index.html").read_text()


@pytest.mark.parametrize(
    "dest",
    ["nfsn:/home/public", "nfsn:/home/public/", "/home/public/birds", "nfsn:birds",
     "nfsn:/home/public/birds/img", ":/home/public/birds"],
)  # fmt: skip
def test_push_refuses_anything_but_a_birds_folder(dest):
    with pytest.raises(ValueError):
        publish._target(dest)


def test_push_target():
    assert publish._target("nfsn:/home/public/birds/") == ("nfsn", "/home/public/birds")


def test_push_deletes_only_stale_page_images(tmp_path, monkeypatch):
    out = tmp_path / "site"
    (out / "img").mkdir(parents=True)
    for name in ("1.jpg", "1-t.jpg", "index.html", "birds.css", ".htaccess"):
        (out / "img" / name if name.startswith("1") else out / name).write_text("x")
    calls = []

    def fake_run(cmd):
        calls.append(cmd)
        if cmd[-1].startswith("ls "):
            return "1.jpg\n1-t.jpg\n2.jpg\n2-t.jpg\nnotes.txt\n"
        return ""

    monkeypatch.setattr(publish, "_run", fake_run)
    assert publish.push(out, "nfsn:/home/public/birds") == 2
    assert calls[-1][-1] == "cd /home/public/birds/img && rm -f -- 2-t.jpg 2.jpg"
    rsyncs = [c for c in calls if c[0] == "rsync"]
    assert rsyncs[0][-1] == "nfsn:/home/public/birds/img/"  # images before the page
    assert rsyncs[1][-1] == "nfsn:/home/public/birds/"


@pytest.mark.parametrize(
    ("box", "expected"),
    [
        (None, (0, 0, 3840, 2160)),
        ((1800, 1000, 2000, 1200), (1036, 614, 2764, 1586)),  # small bird: 45% of the width
        ((0, 0, 200, 200), (0, 0, 1728, 972)),  # in a corner: pushed back inside
        ((100, 100, 3800, 2100), (0, 0, 3840, 2160)),  # huge: the whole frame
    ],
)
def test_thumb_region(box, expected):
    left, top, right, bottom = publish.thumb_region((3840, 2160), box)
    assert (left, top, right, bottom) == expected
    assert abs((right - left) / (bottom - top) - 16 / 9) < 0.01
