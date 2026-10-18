import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "hygiene", Path(__file__).resolve().parent.parent / "scripts" / "hygiene.py"
)
hygiene = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hygiene)


def test_index_has_no_secrets_or_data():
    assert hygiene.problems() == []


def test_forbidden_paths():
    bad = [
        ".env",
        ".env.bak",
        "config/.env.local",
        "data/x.txt",
        "fountain_buddy.db",
        "a/b.JPG",
        "best.pt",
        "head.joblib",
        "launchd/com.fountainbuddy.plist",
    ]
    good = [".env.example", "launchd/com.fountainbuddy.plist.example", "fountain_buddy/db.py"]
    assert all(hygiene.FORBIDDEN_PATH.search(p) for p in bad)
    assert not any(hygiene.FORBIDDEN_PATH.search(p) for p in good)


def test_secret_patterns():
    webhook = "https://discord.com/api/webhooks/123456789012345678/" + "a" * 68
    token = "M" + "a" * 25 + ".Gabcde." + "b" * 38
    assert hygiene.SECRET_PATTERNS["discord webhook URL"].search(webhook)
    assert hygiene.SECRET_PATTERNS["discord bot token"].search(token)


def test_env_secrets_skips_public_keys_and_short_values(tmp_path):
    env = tmp_path / ".env"
    env.write_text(
        "# Camera settings = see docs\n"
        "CAMERA_HOST=192.168.50.249\nCAMERA_PASSWORD='hunter2hunter2'\nX=short\n"
        "# OLD_PASSWORD=retired-but-real\n"
    )
    assert hygiene.env_secrets(env) == {
        "CAMERA_PASSWORD": "hunter2hunter2",
        "OLD_PASSWORD": "retired-but-real",
    }
