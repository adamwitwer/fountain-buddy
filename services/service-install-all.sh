#!/bin/bash
# Install both Fountain Buddy services (main app + Discord bot)

set -e

PROJECT_DIR="/Users/adam/Documents/Projects/fountain-buddy"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"

MAIN_SERVICE="com.fountainbuddy.service"
BOT_SERVICE="com.fountainbuddy.discordbot"

echo "🐦 Installing Fountain Buddy Complete System..."
echo "==============================================="

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCHD_DIR"

# Install main service
echo "📹 Installing camera monitoring service..."
cp "$PROJECT_DIR/services/com.fountainbuddy.service.plist" "$LAUNCHD_DIR/"
launchctl load "$LAUNCHD_DIR/com.fountainbuddy.service.plist"
launchctl enable "gui/$(id -u)/$MAIN_SERVICE"

# Install Discord bot service  
echo "💬 Installing Discord bot service..."
cp "$PROJECT_DIR/services/com.fountainbuddy.discordbot.plist" "$LAUNCHD_DIR/"
launchctl load "$LAUNCHD_DIR/com.fountainbuddy.discordbot.plist"
launchctl enable "gui/$(id -u)/$BOT_SERVICE"

echo ""
echo "✅ Fountain Buddy system installed successfully!"
echo ""
echo "🔧 Two Services Running:"
echo "  1. Camera Monitor  - Detects birds, takes photos"
echo "  2. Discord Bot     - Handles human feedback"
echo ""
echo "📊 Service Management:"
echo "  Status:    ./service-status-all.sh"
echo "  Stop All:  ./service-stop-all.sh"
echo "  Start All: ./service-start-all.sh"
echo "  Logs:      ./service-logs-all.sh"
echo "  Uninstall: ./service-uninstall-all.sh"
echo ""
echo "📂 Log Files:"
echo "  Camera:    logs/fountain-buddy.log"
echo "  Discord:   logs/discord-bot.log"
echo "  Errors:    logs/*-error.log"
echo ""
echo "🚀 Both services are now running and will auto-start at login!"