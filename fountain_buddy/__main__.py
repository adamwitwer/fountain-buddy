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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="fountain-buddy")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="sanity-check settings and log in to the camera")
    args = parser.parse_args(argv)

    if args.command == "check":
        return check()
    return 2


if __name__ == "__main__":
    sys.exit(main())
