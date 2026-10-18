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


def train_head() -> int:
    import json
    import logging

    from fountain_buddy import classifier

    logging.basicConfig(level=logging.INFO)
    cfg = settings()
    path = classifier.train_head(cfg.db_path, cfg.data_dir)
    meta = json.loads((cfg.models_dir / "head.json").read_text())
    print(f"head: {path.name} on {meta['labels']} labels + {meta['nabirds']} NABirds")
    print("held-out:", {k: round(v, 3) for k, v in meta["heldout"].items()})
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
    sub.add_parser("train-head", help="retrain the species classifier on every label")
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
    if args.command == "run":
        from fountain_buddy import service

        return service.main()
    if args.command == "train-head":
        return train_head()
    if args.command == "post-test":
        return post_test(args.image)
    if args.command == "bakeoff":
        return bakeoff(args.models, args.detectors)
    return 2


if __name__ == "__main__":
    sys.exit(main())
