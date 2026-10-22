"""Command line: `uv run fountain-buddy <command>` (or `python -m fountain_buddy`)."""

from __future__ import annotations

import argparse
import asyncio
import sys

from fountain_buddy.config import settings


async def _check_camera() -> bool:
    from reolink_aio.api import Host

    cfg = settings()
    host = Host(cfg.camera_host, cfg.camera_username, cfg.camera_password, timeout=15)
    try:
        await host.get_host_data()
        print(
            f"camera: {host.camera_name(0)!r} {host.camera_model(0)} "
            f"firmware {host.camera_sw_version(0)} at {cfg.camera_host}"
        )
        snap = await host.get_snapshot(0, stream="main")
        print(f"snapshot: {len(snap) if snap else 0} bytes")
        return bool(snap)
    except Exception as exc:  # report, don't crash: this is a diagnostic
        print(f"camera: FAILED at {cfg.camera_host}: {type(exc).__name__}: {exc}")
        return False
    finally:
        await host.logout()


def check() -> int:
    cfg = settings()
    print(f"data dir: {cfg.data_dir} (exists: {cfg.data_dir.exists()})")
    print(f"camera password set: {bool(cfg.camera_password)}")
    print(f"discord token set: {bool(cfg.discord_token)}")
    print(f"discord channel set: {cfg.discord_channel_id is not None}")
    print(f"healthcheck url set: {bool(cfg.healthcheck_url)}")
    camera_ok = asyncio.run(_check_camera())
    return 0 if camera_ok else 1


def import_legacy() -> int:
    from fountain_buddy import legacy

    cfg = settings()
    counts = legacy.import_visits(cfg.data_dir / "legacy.db", cfg.db_path)
    print("import:", counts)
    counts = legacy.extract_crops(cfg.db_path, cfg.data_dir)
    print("crops:", counts)
    return 0


def status() -> int:
    """Terminal check for when the bot doesn't answer `status` in Discord."""
    import datetime as dt
    import os
    import re
    import socket
    import subprocess

    cfg = settings()
    label = f"gui/{os.getuid()}/com.fountainbuddy.run"
    out = subprocess.run(["launchctl", "print", label], capture_output=True, text=True)
    ok = True
    if out.returncode != 0:
        print("launchd: NOT LOADED. Fix: launchd/install.sh")
        ok = False
    else:
        fields = dict(
            re.findall(r"^\t(state|pid|runs|last exit code|last terminating signal) = (.+)$",
                       out.stdout, re.M)
        )  # fmt: skip
        last = fields.get("last exit code") or fields.get("last terminating signal")
        tail = f", last exit: {last}" if last else ""
        print(f"launchd: {fields.get('state')}, pid {fields.get('pid', '-')}, "
              f"started {fields.get('runs')} times{tail}")  # fmt: skip
        ok = fields.get("state") == "running"

    log = cfg.data_dir / "logs" / "fountain-buddy.log"
    lines = log.read_text(errors="ignore").splitlines() if log.exists() else []
    started = [ln for ln in lines if "service: running" in ln]
    print(f"last start: {started[-1][:19] if started else 'never'}")
    print(f"last log line: {lines[-1][:19] if lines else 'none'}")
    since = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    problems = [
        ln for ln in lines
        if ln[:16] >= since and (" WARNING " in ln or " ERROR " in ln)
        and "voice will NOT be supported" not in ln
    ]  # fmt: skip
    for ln in problems[-5:]:
        print("  " + ln[:160])

    try:
        socket.create_connection((cfg.camera_host, 443), timeout=3).close()
        print(f"camera: answers at {cfg.camera_host}")
    except OSError as exc:
        print(f"camera: NOT reachable at {cfg.camera_host} ({exc}). Check its power and Wi-Fi.")
        ok = False

    if ok:
        print("verdict: running. If Discord's `status` still gets no reply, restart it:")
    else:
        print("verdict: not healthy. Restart it:")
    print("  launchd/install.sh   (then look for a permission dialog on the Mini's screen)")
    return 0 if ok else 1


def post_test(image: str) -> int:
    import cv2

    from fountain_buddy import legacy
    from fountain_buddy.bot import FeederBot
    from fountain_buddy.service import load_pipeline

    cfg = settings()
    pipeline = load_pipeline(cfg, camera="test", source="test")
    frame = legacy.remove_overlays(cv2.imread(image))
    sighting = pipeline.process([frame])
    if sighting is None:
        print("no bird found in that image")
        return 1
    print("top guesses:", [(label, round(p, 3)) for label, p in sighting.ranked[:3]])

    async def go():
        bot = FeederBot(cfg.db_path, cfg.discord_channel_id)
        task = asyncio.create_task(bot.start(cfg.discord_token))
        await asyncio.wait_for(bot.ready.wait(), 60)
        message = await bot.post(sighting.visit_id, sighting.preview_path)
        print(f"posted visit {sighting.visit_id}: {message.jump_url}")
        await bot.close()
        task.cancel()

    asyncio.run(go())
    return 0


def train_head(force: bool) -> int:
    import logging

    from fountain_buddy import classifier, db

    logging.basicConfig(level=logging.INFO)
    cfg = settings()
    db.init(cfg.db_path)
    result = classifier.retrain(cfg.db_path, cfg.data_dir, force=force)
    print(f"{result.reason}; current head: {result.head} ({result.new_labels} new labels)")
    if result.gate:
        for side in ("incumbent", "candidate"):
            m = result.gate[side]
            print(f"  gate {side}: top-1 {m['top1']:.1%}, top-3 {m['top3']:.1%} "
                  f"on {result.gate['n']} crops")  # fmt: skip
        for k, f in result.gate["flips"].items():
            print(f"  {k}: {f['worse']} crops worse, {f['better']} better, p={f['p']:.3f}")
    return 0 if result.accepted or result.reason == "no new labels" else 1


def report() -> int:
    import datetime as dt

    from fountain_buddy import db
    from fountain_buddy import report as rep

    cfg = settings()
    db.init(cfg.db_path)
    print(rep.weekly_text(cfg.db_path, cfg.models_dir, dt.date.today()) or "nothing posted")
    return 0


def bakeoff(models: list[str], detectors: bool = False) -> int:
    import datetime as dt

    from fountain_buddy import bakeoff as bake

    cfg = settings()
    if detectors:
        text, stem = bake.detection_recall(cfg.db_path, cfg.data_dir), "detectors"
    else:
        text, stem = bake.run(cfg.db_path, cfg.data_dir, models), "bakeoff"
    out = cfg.data_dir / "reports" / f"{stem}-{dt.date.today().isoformat()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(text)
    print(f"report: {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="fountain-buddy")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="sanity-check settings and log in to the camera")
    sub.add_parser(
        "import-legacy", help="import v1's visits and labels, and crop labeled photos (idempotent)"
    )
    sub.add_parser("run", help="run the service: camera, models, Discord")
    sub.add_parser("status", help="is the service up? (launchd, log, camera)")
    p = sub.add_parser(
        "train-head",
        help="retrain the classifier (gated; the service does this by itself after answers)",
    )
    p.add_argument("--force", action="store_true", help="accept even if it scores worse")
    sub.add_parser("report", help="the weekly agreement report, for the last 7 days")
    p = sub.add_parser("post-test", help="post one image to Discord as a TEST sighting")
    p.add_argument("image", help="a frame (v1 overlays are painted out first)")
    p = sub.add_parser("bakeoff", help="compare classifier backbones on the labeled crops")
    p.add_argument("--models", nargs="+", default=["bioclip2", "dinov3-l", "dinov3-b"])
    p.add_argument("--detectors", action="store_true", help="compare detectors instead")
    args = parser.parse_args(argv)

    if args.command == "check":
        return check()
    if args.command == "import-legacy":
        return import_legacy()
    if args.command == "status":
        return status()
    if args.command == "run":
        from fountain_buddy import service

        return service.main()
    if args.command == "train-head":
        return train_head(args.force)
    if args.command == "report":
        return report()
    if args.command == "post-test":
        return post_test(args.image)
    if args.command == "bakeoff":
        return bakeoff(args.models, args.detectors)
    return 2


if __name__ == "__main__":
    sys.exit(main())
