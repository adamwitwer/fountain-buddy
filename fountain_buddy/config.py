"""Settings, read from the environment (and `.env` in the repo root) when first asked for.

Read lazily: nothing env-derived is captured at import time, so tests and tools can set
the environment first. Never print a secret; check it with `bool(...)`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    camera_host: str
    camera_username: str
    camera_password: str = ""
    discord_token: str = ""
    discord_channel_id: int | None = None
    healthcheck_url: str = ""
    publish_dest: str = ""  # host:/path/birds for the public page; empty: build only
    data_dir: Path = REPO_ROOT / "data"

    @property
    def images_dir(self) -> Path:
        return self.data_dir / "images"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "fountain_buddy.db"

    @property
    def models_dir(self) -> Path:
        return self.data_dir / "models"


@cache
def settings() -> Settings:
    load_dotenv(REPO_ROOT / ".env", override=False)
    channel = os.getenv("DISCORD_CHANNEL_ID", "").strip()
    data_dir = os.getenv("FB_DATA_DIR", "").strip()
    return Settings(
        camera_host=os.getenv("CAMERA_HOST", "192.168.50.249"),
        camera_username=os.getenv("CAMERA_USERNAME", "admin"),
        camera_password=os.getenv("CAMERA_PASSWORD", ""),
        discord_token=os.getenv("DISCORD_BOT_TOKEN", ""),
        discord_channel_id=int(channel) if channel else None,
        healthcheck_url=os.getenv("HEALTHCHECK_URL", ""),
        publish_dest=os.getenv("FB_PUBLISH_DEST", "").strip(),
        data_dir=Path(data_dir) if data_dir else REPO_ROOT / "data",
    )
