"""The public page: answered sightings, rendered to static files and pushed to the web
host (adamwitwer.com/birds/). `fountain-buddy publish` runs it; the service runs it after
each run of answers.

Only visits Adam answered with a species (or Squirrel) are published, so every photo on
the page is one a human has looked at. Skip, Not a bird and unanswered posts never are.
Each guess shown was made before its answer existed, like the weekly report's.

Photos are the full frame, downsized: the bird is too close for the lens to focus, so a
tight crop is blurry at any size, but the whole scene reads fine at web width. Thumbnails
are a loose 16:9 crop around the bird, so a small one still shows up.
"""

from __future__ import annotations

import datetime as dt
import html
import logging
import re
import shlex
import shutil
import subprocess
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from fountain_buddy import db, report, species
from fountain_buddy.config import Settings

log = logging.getLogger(__name__)

KEEP_DAYS = 10  # visits shown; each visitor's best photo stays regardless
VISIT_GAP = dt.timedelta(minutes=10)  # same visitor within this is one visit
FULL_WIDTH = 1280
THUMB_WIDTH = 480
THUMB_MIN_SHARE = 0.45  # a thumbnail shows at least this share of the frame's width
VISITORS = [*species.SPECIES, species.SQUIRREL]
SITE = Path(__file__).parent / "site"  # birds.css and .htaccess, copied as-is
IMAGE_NAME = re.compile(r"^\d+(-t)?\.jpg$")
TONES = ("amber", "blue")


@dataclass(frozen=True)
class Photo:
    visit_id: int
    taken_at: dt.datetime
    label: str
    image_path: str
    det_conf: float
    guess: str | None
    guess_p: float | None
    box: tuple[int, int, int, int] | None = None  # the best crop's, in frame pixels

    @property
    def agreed(self) -> bool:
        return self.guess == self.label


@dataclass
class Visit:
    label: str
    photos: list[Photo]

    @property
    def best(self) -> Photo:
        return max(self.photos, key=lambda p: p.det_conf)

    @property
    def start(self) -> dt.datetime:
        return self.photos[0].taken_at

    @property
    def end(self) -> dt.datetime:
        return self.photos[-1].taken_at


@dataclass(frozen=True)
class Visitor:
    label: str
    visits: int
    photos: int
    first_seen: dt.datetime
    best: Photo


def load_photos(store: Path) -> list[Photo]:
    """Answered live tray photos whose current label is a visitor, oldest first."""
    with closing(db.connect(store)) as conn:
        rows = conn.execute(
            "SELECT v.id, v.taken_at, v.image_path, l.label, c.det_conf, "
            "c.x1, c.y1, c.x2, c.y2, p.label AS guess, p.confidence AS guess_p "
            "FROM visits v JOIN current_labels l ON l.visit_id = v.id "
            "LEFT JOIN crops c ON c.id = (SELECT id FROM crops WHERE visit_id = v.id "
            "ORDER BY det_conf DESC LIMIT 1) "
            "LEFT JOIN predictions p "
            "ON p.id = (SELECT MAX(id) FROM predictions WHERE visit_id = v.id) "
            "WHERE v.source = 'live' AND v.camera = 'tray' AND v.image_path IS NOT NULL "
            "ORDER BY v.taken_at, v.id"
        ).fetchall()
    return [
        Photo(r["id"], dt.datetime.fromisoformat(r["taken_at"]), r["label"], r["image_path"],
              r["det_conf"] or 0.0, r["guess"], r["guess_p"],
              (r["x1"], r["y1"], r["x2"], r["y2"]) if r["x1"] is not None else None)
        for r in rows
        if r["label"] in VISITORS
    ]  # fmt: skip


def group_visits(photos: list[Photo]) -> list[Visit]:
    """Runs of one visitor with no gap over VISIT_GAP, newest visit first. Another
    species arriving in between doesn't split a visit."""
    visits: list[Visit] = []
    open_visit: dict[str, Visit] = {}
    for photo in sorted(photos, key=lambda p: p.taken_at):
        current = open_visit.get(photo.label)
        if current and photo.taken_at - current.end <= VISIT_GAP:
            current.photos.append(photo)
        else:
            current = open_visit[photo.label] = Visit(photo.label, [photo])
            visits.append(current)
    return sorted(visits, key=lambda v: v.end, reverse=True)


def visitors(visits: list[Visit]) -> list[Visitor]:
    """One entry per visitor ever seen, most visits first."""
    out = []
    for label in {v.label for v in visits}:
        mine = [v for v in visits if v.label == label]
        photos = [p for v in mine for p in v.photos]
        out.append(Visitor(label, len(mine), len(photos), min(v.start for v in mine),
                           max(photos, key=lambda p: p.det_conf)))  # fmt: skip
    return sorted(out, key=lambda s: (-s.visits, s.label))


# ---------- images ----------


def thumb_region(size: tuple[int, int], box) -> tuple[int, int, int, int]:
    """A 16:9 region around the box, three times its size but at least THUMB_MIN_SHARE
    of the frame's width, kept inside the frame."""
    width, height = size
    if not box:
        return 0, 0, width, height
    x1, y1, x2, y2 = box
    w = max(3 * (x2 - x1), 3 * (y2 - y1) * 16 / 9, THUMB_MIN_SHARE * width)
    w = min(w, width, height * 16 / 9)
    h = w * 9 / 16
    left = min(max((x1 + x2) / 2 - w / 2, 0), width - w)
    top = min(max((y1 + y2) / 2 - h / 2, 0), height - h)
    return round(left), round(top), round(left + w), round(top + h)


def _write_images(photo: Photo, data_dir: Path, img_dir: Path) -> None:
    """The page's two sizes of a photo. Frames never change, so existing files are kept.
    Pillow writes no EXIF unless asked, so nothing from the camera rides along."""
    full, thumb = img_dir / f"{photo.visit_id}.jpg", img_dir / f"{photo.visit_id}-t.jpg"
    if full.exists() and thumb.exists():
        return
    with Image.open(data_dir / photo.image_path) as im:
        im = im.convert("RGB")
        cut = im.crop(thumb_region(im.size, photo.box))
        for path, source, width, quality in ((full, im, FULL_WIDTH, 80),
                                             (thumb, cut, THUMB_WIDTH, 75)):  # fmt: skip
            small = source.resize((width, round(source.height * width / source.width)),
                                  Image.LANCZOS)  # fmt: skip
            small.save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def _size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


# ---------- page ----------


def _e(text: object) -> str:
    return html.escape(str(text), quote=True)


def _time(t: dt.datetime) -> str:
    return f"{t:%-I:%M} {'am' if t.hour < 12 else 'pm'}"


def _when(t: dt.datetime) -> str:
    return f"{t:%a %b %-d}, {_time(t)}"


def _guess_text(label: str | None) -> str:
    if label == species.SKIP:
        return "a photo too blurry to use"
    if label == species.NOT_A_BIRD:
        return "not a bird"
    return label or "nothing"


def _verdict(visit: Visit) -> tuple[str, str]:
    """(css class, short text) for a visit's chip, from its best photo's guess."""
    best = visit.best
    if best.agreed:
        return "agree", f"AI agreed ({best.guess_p:.0%})" if best.guess_p else "AI agreed"
    return "miss", f"AI guessed {_guess_text(best.guess)}"


def _verdict_long(visit: Visit) -> str:
    best = visit.best
    if best.agreed:
        line = f"The AI guessed {_e(best.label)} too"
        line += f" ({best.guess_p:.0%} sure)." if best.guess_p else "."
    else:
        line = f"The AI guessed {_e(_guess_text(best.guess))}. I said {_e(best.label)}."
    if len(visit.photos) > 1:
        right = sum(p.agreed for p in visit.photos)
        line += f" Across the visit it got {right} of {len(visit.photos)} photos right."
    return line


def _length(visit: Visit) -> str:
    n = len(visit.photos)
    if n == 1:
        return "1 photo"
    minutes = max(1, round((visit.end - visit.start).total_seconds() / 60))
    return f"{n} photos over {minutes} min"


def _img(photo: Photo, img_dir: Path, thumb: bool, alt: str, lazy: bool = True) -> str:
    name = f"{photo.visit_id}-t.jpg" if thumb else f"{photo.visit_id}.jpg"
    w, h = _size(img_dir / name)
    loading = ' loading="lazy"' if lazy else ""
    return (f'<a href="img/{photo.visit_id}.jpg"><img src="img/{name}" width="{w}" '
            f'height="{h}" alt="{_e(alt)}"{loading}></a>')  # fmt: skip


def _alt(photo: Photo) -> str:
    return f"{photo.label} at the tray feeder, {_when(photo.taken_at)}"


def _score(store: Path, today: dt.date) -> str:
    rows = report.answered(store, today - dt.timedelta(days=6), today + dt.timedelta(days=1))
    birds = [r for r in rows if r["label"] in species.SPECIES]
    if not birds:
        return ""
    right = sum(r["guess"] == r["label"] for r in birds)
    return (f"<p>Over the last 7 days the AI's first guess matched mine on {right} of "
            f"{len(birds)} birds ({right / len(birds):.0%}).</p>")  # fmt: skip


def render(visits: list[Visit], everyone: list[Visitor], img_dir: Path, now: dt.datetime,
           score: str) -> str:  # fmt: skip
    recent = [v for v in visits if v.end >= now - dt.timedelta(days=KEEP_DAYS)]
    parts = [
        '<header class="intro-block">',
        '<p class="back"><a href="/">← adamwitwer.com</a></p>',
        '<p class="hello">Fountain Buddy</p>',
        "<h1>Who’s at the tray</h1>",
        '<p class="intro">A camera watches a tray feeder full of safflower seed. An AI '
        "guesses who dropped by, I tell it when it’s wrong, and it learns from every "
        "answer. I’ve checked every photo here. The camera is still finding its best "
        "angle, so forgive the soft focus.</p>",
        f'<p class="updated">Updated {_e(_when(now))}.</p>',
        "</header>",
    ]
    if not recent:
        parts.append(f'<p class="lede">No visitors in the last {KEEP_DAYS} days. '
                     "Quiet tray.</p>")  # fmt: skip
    else:
        latest = recent[0]
        tone, _ = _verdict(latest)
        parts += [
            '<section class="latest" aria-labelledby="latest-h">',
            '<h2 id="latest-h" class="eyebrow">Latest visit</h2>',
            "<figure>",
            _img(latest.best, img_dir, thumb=False, alt=_alt(latest.best), lazy=False),
            "<figcaption>",
            f'<p class="name">{_e(latest.label)}</p>',
            f'<p class="meta">{_e(_when(latest.start))} · {_e(_length(latest))}</p>',
            f'<p class="ai {tone}">{_verdict_long(latest)}</p>',
            "</figcaption></figure></section>",
        ]

    if everyone:
        parts += [
            '<section aria-labelledby="who-h">',
            '<h2 id="who-h">Who’s been by</h2>',
            f'<p class="lede">{len(everyone)} kinds of visitor so far, each with its best '
            "photo.</p>",
            '<ul class="tiles">',
        ]
        for s in everyone:
            visits_word = "visit" if s.visits == 1 else "visits"
            parts += [
                '<li class="tile">',
                _img(s.best, img_dir, thumb=True, alt=_alt(s.best)),
                f"<h3>{_e(s.label)}</h3>",
                f"<p>{s.visits} {visits_word} · first seen {s.first_seen:%b %-d}</p>",
                "</li>",
            ]
        parts.append("</ul></section>")

    if recent:
        parts += [
            '<section aria-labelledby="days-h">',
            f'<h2 id="days-h">The last {KEEP_DAYS} days</h2>',
        ]
        days: dict[dt.date, list[Visit]] = {}
        for v in recent:
            days.setdefault(v.end.date(), []).append(v)
        for i, (day, day_visits) in enumerate(days.items()):
            n = len(day_visits)
            parts += [
                f'<div class="group" data-tone="{TONES[i % 2]}">',
                f"<h3>{day:%A, %B %-d} <span>{n} visit{'s' if n != 1 else ''}</span></h3>",
                '<ul class="visits">',
            ]
            for v in day_visits:
                tone, text = _verdict(v)
                parts += [
                    '<li class="visit">',
                    _img(v.best, img_dir, thumb=True, alt=_alt(v.best)),
                    f"<h4>{_e(v.label)}</h4>",
                    f'<p class="meta">{_e(_time(v.start))} · {_e(_length(v))}</p>',
                    f'<p class="ai {tone}">{_e(text)}</p>',
                    "</li>",
                ]
            parts.append("</ul></div>")
        parts.append("</section>")

    parts += [
        "<footer>",
        score,
        '<p><a href="https://github.com/adamwitwer/fountain-buddy">How it works ↗</a></p>',
        "</footer>",
    ]
    body = "\n".join(parts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Who’s at the tray · Adam Witwer</title>
<meta name="description" content="Birds at my tray feeder, identified by an AI and checked by me.">
<link rel="icon" href="/assets/si.png">
<link rel="stylesheet" href="/css/site.css">
<link rel="stylesheet" href="birds.css">
</head>
<body>
<main class="wrap birds">
{body}
</main>
</body>
</html>
"""


# ---------- build and push ----------


def build(store: Path, data_dir: Path, out: Path, now: dt.datetime | None = None) -> Path:
    """Render the page and its images into `out`. Removes images the page no longer
    uses, so `out/img` is exactly what the server should hold."""
    now = now or dt.datetime.now()
    img_dir = out / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    visits = group_visits(load_photos(store))
    everyone = visitors(visits)
    cutoff = now - dt.timedelta(days=KEEP_DAYS)
    shown = [v.best for v in visits if v.end >= cutoff] + [s.best for s in everyone]
    for photo in shown:
        _write_images(photo, data_dir, img_dir)
    keep = {name for p in shown for name in (f"{p.visit_id}.jpg", f"{p.visit_id}-t.jpg")}
    for path in img_dir.iterdir():
        if path.name not in keep:
            path.unlink()
    page = render(visits, everyone, img_dir, now, _score(store, now.date()))
    (out / "index.html.tmp").write_text(page)
    (out / "index.html.tmp").replace(out / "index.html")
    for name in ("birds.css", ".htaccess"):
        shutil.copyfile(SITE / name, out / name)
    log.info("publish: built %d visits, %d visitors, %d images", len(visits), len(everyone),
             len(keep))  # fmt: skip
    return out


def _target(dest: str) -> tuple[str, str]:
    """Split `host:/path/birds`. Refuses any other folder: the push deletes stale
    images, and must never be pointed at the site root."""
    host, sep, path = dest.partition(":")
    path = path.rstrip("/")
    if not (host and sep and path.startswith("/") and path.endswith("/birds")):
        raise ValueError(f"FB_PUBLISH_DEST must look like host:/abs/path/birds, not {dest!r}")
    return host, path


def _run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed ({result.returncode}): {result.stderr.strip()}")
    return result.stdout


def push(out: Path, dest: str) -> int:
    """Upload images first, then the page, then delete images it no longer uses.
    Returns the number deleted. BatchMode: fail rather than wait on a prompt."""
    host, path = _target(dest)
    ssh = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20", host]
    remote_img = f"{path}/img"
    _run([*ssh, f"mkdir -p {shlex.quote(remote_img)}"])
    rsync = ["rsync", "-rtz", "-e", "ssh -o BatchMode=yes -o ConnectTimeout=20"]
    _run([*rsync, f"{out / 'img'}/", f"{host}:{remote_img}/"])
    pages = [str(out / name) for name in ("birds.css", ".htaccess", "index.html")]
    _run([*rsync, "--checksum", *pages, f"{host}:{path}/"])

    local = {p.name for p in (out / "img").iterdir()}
    remote = set(_run([*ssh, f"ls -1 {shlex.quote(remote_img)}"]).split())
    stale = sorted(n for n in remote - local if IMAGE_NAME.match(n))
    for i in range(0, len(stale), 200):
        names = " ".join(shlex.quote(n) for n in stale[i : i + 200])
        _run([*ssh, f"cd {shlex.quote(remote_img)} && rm -f -- {names}"])
    return len(stale)


def publish(cfg: Settings, upload: bool = True) -> str:
    """Build, and push if FB_PUBLISH_DEST is set. Returns a one-line summary."""
    out = build(cfg.db_path, cfg.data_dir, cfg.data_dir / "site" / "birds")
    if not upload:
        return f"built {out / 'index.html'} (not uploaded)"
    if not cfg.publish_dest:
        return f"built {out / 'index.html'}; FB_PUBLISH_DEST is not set, so not uploaded"
    removed = push(out, cfg.publish_dest)
    log.info("publish: pushed to %s, removed %d old images", cfg.publish_dest, removed)
    return f"published to {cfg.publish_dest} ({removed} old images removed)"
