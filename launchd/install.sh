#!/bin/bash
# Install (or reinstall) the Fountain Buddy LaunchAgent, or remove it.
#   launchd/install.sh            install / restart with the current code
#   launchd/install.sh uninstall  stop and remove
set -euo pipefail

LABEL=com.fountainbuddy.run
REPO="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true

if [[ "${1:-}" == "uninstall" ]]; then
    rm -f "$TARGET"
    echo "removed $LABEL"
    exit 0
fi

[[ -x "$REPO/.venv/bin/python" ]] || { echo "no .venv: run 'uv sync' first" >&2; exit 1; }
[[ -f "$REPO/.env" ]] || { echo "no .env in $REPO" >&2; exit 1; }

sed -e "s#__REPO__#$REPO#g" -e "s#__HOME__#$HOME#g" \
    "$REPO/launchd/$LABEL.plist.example" > "$TARGET"
plutil -lint "$TARGET" >/dev/null

launchctl enable "$DOMAIN/$LABEL"
launchctl bootstrap "$DOMAIN" "$TARGET"
echo "installed $LABEL; logs: $REPO/data/logs/fountain-buddy.log"
