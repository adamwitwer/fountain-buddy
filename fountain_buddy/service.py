"""The long-running service: camera motion → burst → pipeline → Discord, plus the daily
summary and liveness. One process, one asyncio loop. Models run on one worker thread.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import json
import logging
import logging.handlers
import sys
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing, suppress

from fountain_buddy import db, species
from fountain_buddy.bot import FeederBot
from fountain_buddy.camera import Camera
from fountain_buddy.classifier import Classifier
from fountain_buddy.config import Settings, settings
from fountain_buddy.detect import Detector
from fountain_buddy.pipeline import Pipeline

log = logging.getLogger("fountain_buddy")

POST_COOLDOWN_SECONDS = 45
SUMMARY_AT = dt.time(20, 0)
HEALTH_EVERY_SECONDS = 300
CAMERA_DOWN_ALERT_SECONDS = 15 * 60

# Used until data/models/detector.json names something better (the fine-tuned weights).
DEFAULT_DETECTOR = {"weights": "yolo26m.pt", "imgsz": 1280, "conf": 0.1}


def setup_logging(cfg: Settings) -> None:
    logs = cfg.data_dir / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    file = logging.handlers.RotatingFileHandler(
        logs / "fountain-buddy.log", maxBytes=5_000_000, backupCount=5
    )
    console = logging.StreamHandler()
    # Under launchd stderr is a file that never rotates; keep it to warnings and up.
    console.setLevel(logging.INFO if sys.stderr.isatty() else logging.WARNING)
    for handler in (file, console):
        handler.setFormatter(fmt)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [file, console]
    for noisy in ("discord.gateway", "discord.client", "reolink_aio", "httpx"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def detector_config(cfg: Settings) -> dict:
    pointer = cfg.models_dir / "detector.json"
    return json.loads(pointer.read_text()) if pointer.exists() else DEFAULT_DETECTOR


def summary_text(store, day: dt.date) -> str | None:
    start, end = day.isoformat(), (day + dt.timedelta(days=1)).isoformat()
    with closing(db.connect(store)) as conn:
        rows = conn.execute(
            "SELECT v.id, l.label, p.label AS guess FROM visits v "
            "JOIN posts ON posts.visit_id = v.id "
            "LEFT JOIN current_labels l ON l.visit_id = v.id "
            "LEFT JOIN predictions p "
            "ON p.id = (SELECT MAX(id) FROM predictions WHERE visit_id = v.id) "
            "WHERE v.source = 'live' AND v.taken_at >= ? AND v.taken_at < ?",
            (start, end),
        ).fetchall()
    if not rows:
        return None
    labeled = [r for r in rows if r["label"]]
    birds = Counter(r["label"] for r in labeled if r["label"] in species.SPECIES)
    right = sum(r["label"] == r["guess"] for r in labeled if r["label"] != species.SKIP)
    judged = sum(r["label"] != species.SKIP for r in labeled)
    lines = [
        f"**Today at the tray** ({day:%a %b %-d}): {len(rows)} photos, {len(labeled)} answered"
    ]
    lines += [f"• {name}: {n}" for name, n in birds.most_common()]
    if judged:
        lines.append(f"Model agreed with you on {right}/{judged} ({right / judged:.0%}).")
    if len(rows) > len(labeled):
        lines.append(f"{len(rows) - len(labeled)} still unanswered.")
    return "\n".join(lines)


def load_pipeline(cfg: Settings, **kwargs) -> Pipeline:
    det = detector_config(cfg)
    detector = Detector(cfg.models_dir, det["weights"], det["imgsz"], det["conf"])
    classifier = Classifier(cfg.models_dir)
    classifier.version  # noqa: B018 - loads the head now, not on the first bird
    log.info("models: detector %s (conf %.2f), classifier %s",
             detector.name, det["conf"], classifier.version)  # fmt: skip
    return Pipeline(cfg.db_path, cfg.data_dir, detector, classifier, **kwargs)


class Service:
    """Construct inside the event loop: the camera client needs a running loop."""

    def __init__(self, cfg: Settings):
        self.cfg = cfg
        self.bot = FeederBot(cfg.db_path, cfg.discord_channel_id)
        self.camera = Camera(cfg.camera_host, cfg.camera_username, cfg.camera_password)
        self.worker = ThreadPoolExecutor(max_workers=1, thread_name_prefix="models")
        self.pipeline: Pipeline | None = None
        self.last_post = 0.0
        self.camera_alerted = False

    async def on_motion(self) -> None:
        if time.time() - self.last_post < POST_COOLDOWN_SECONDS:
            return
        frames = await self.camera.burst()
        if not frames:
            return
        loop = asyncio.get_running_loop()
        sighting = await loop.run_in_executor(self.worker, self.pipeline.process, frames)
        if sighting:
            await self.bot.post(sighting.visit_id, sighting.preview_path)
            self.last_post = time.time()

    async def daily(self) -> None:
        while True:
            now = dt.datetime.now()
            at = dt.datetime.combine(now.date(), SUMMARY_AT)
            if at <= now:
                at += dt.timedelta(days=1)
            await asyncio.sleep((at - now).total_seconds())
            text = summary_text(self.cfg.db_path, at.date())
            if text:
                await self.bot.say(text)
            self.pipeline.prune_rejects()

    async def health(self) -> None:
        while True:
            await asyncio.sleep(HEALTH_EVERY_SECONDS)
            down_for = time.time() - self.camera.last_ok
            ok = down_for < CAMERA_DOWN_ALERT_SECONDS and self.bot.is_ready()
            if down_for >= CAMERA_DOWN_ALERT_SECONDS and not self.camera_alerted:
                await self.bot.say(
                    f"⚠️ Can't reach the Tray Feeder camera for {down_for / 60:.0f} min."
                )
                self.camera_alerted = True
            elif down_for < CAMERA_DOWN_ALERT_SECONDS and self.camera_alerted:
                await self.bot.say("✅ Tray Feeder camera is back.")
                self.camera_alerted = False
            if self.cfg.healthcheck_url:
                url = self.cfg.healthcheck_url + ("" if ok else "/fail")
                try:
                    await asyncio.to_thread(urllib.request.urlopen, url, timeout=10)
                except Exception as exc:
                    log.warning("healthcheck ping failed: %s", exc)

    async def run(self) -> None:
        db.init(self.cfg.db_path)
        loop = asyncio.get_running_loop()
        self.pipeline = await loop.run_in_executor(self.worker, load_pipeline, self.cfg)
        bot_task = asyncio.create_task(self.bot.start(self.cfg.discord_token), name="discord")
        await asyncio.wait_for(self.bot.ready.wait(), 60)
        try:
            await self.camera.connect()
        except Exception as exc:  # watch() keeps retrying
            log.warning("camera: initial connect failed: %s", exc)
        tasks = [
            bot_task,
            asyncio.create_task(self.camera.watch(self.on_motion), name="camera"),
            asyncio.create_task(self.daily(), name="daily"),
            asyncio.create_task(self.health(), name="health"),
        ]
        log.info("service: running")
        try:
            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
            for task in done:
                task.result()  # surface the crash so launchd restarts us
        finally:
            for task in tasks:
                task.cancel()
            await self.bot.close()
            with suppress(Exception):
                await self.camera.close()


async def _run(cfg: Settings) -> None:
    await Service(cfg).run()


def main() -> int:
    cfg = settings()
    setup_logging(cfg)
    if not (cfg.discord_token and cfg.discord_channel_id and cfg.camera_password):
        log.error("missing DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID or CAMERA_PASSWORD in .env")
        return 2
    asyncio.run(_run(cfg))
    return 0
