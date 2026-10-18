"""Refuse to let secrets or data into git. This repo is public.

Checks what is in the git index (exactly what the next commit will contain):
- no forbidden paths (.env, databases, images, model weights, launchd plists);
- no file containing a value from the local .env, or a Discord token / webhook URL.

Run directly (`python scripts/hygiene.py`) or via .githooks/pre-commit and the test suite.
Prints paths and key names only, never the matching value.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_PATH = re.compile(
    r"(^|/)\.env($|\.(?!example$))"
    r"|\.(db|sqlite3?|jpe?g|png|pt|pth|safetensors|keras|onnx|npz|npy|joblib|pkl)$"
    r"|\.plist$"
    r"|^data/",
    re.IGNORECASE,
)
SECRET_PATTERNS = {
    "discord webhook URL": re.compile(r"discord(?:app)?\.com/api/webhooks/\d+/[\w-]{20,}"),
    "discord bot token": re.compile(r"\b[MNO][\w-]{23,27}\.[\w-]{6}\.[\w-]{27,}"),
}
# .env keys whose values are not secret and may legitimately appear in the repo.
PUBLIC_ENV_KEYS = {"CAMERA_HOST", "CAMERA_USERNAME", "FB_DATA_DIR", "DISCORD_CHANNEL_ID"}
MIN_SECRET_LEN = 8


def _git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, check=True).stdout


def indexed_files() -> list[str]:
    return [p for p in _git("ls-files", "-z").decode().split("\0") if p]


def env_secrets(env_path: Path = REPO_ROOT / ".env") -> dict[str, str]:
    if not env_path.exists():
        return {}
    secrets = {}
    for line in env_path.read_text().splitlines():
        # Commented-out assignments (`# OLD_PASSWORD=...`) hold real secrets too.
        line = line.strip().lstrip("#").strip()
        if not line or "=" not in line or " " in line.split("=", 1)[0]:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip("'\"")
        if key not in PUBLIC_ENV_KEYS and len(value) >= MIN_SECRET_LEN:
            secrets[key] = value
    return secrets


def problems() -> list[str]:
    found = []
    secrets = env_secrets()
    for path in indexed_files():
        if FORBIDDEN_PATH.search(path):
            found.append(f"{path}: this kind of file must never be tracked")
            continue
        blob = _git("show", f":{path}").decode(errors="ignore")
        for key, value in secrets.items():
            if value in blob:
                found.append(f"{path}: contains the value of .env {key}")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(blob):
                found.append(f"{path}: looks like it contains a {label}")
    return found


def main() -> int:
    found = problems()
    for line in found:
        print(f"hygiene: {line}", file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
