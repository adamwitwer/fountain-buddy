#!/bin/bash
# Uninstall both Fountain Buddy services

MAIN_SERVICE="com.fountainbuddy.service"
BOT_SERVICE="com.fountainbuddy.discordbot"

MAIN_PLIST="$HOME/Library/LaunchAgents/com.fountainbuddy.service.plist"
BOT_PLIST="$HOME/Library/LaunchAgents/com.fountainbuddy.discordbot.plist"

echo "🗑️ Uninstalling Fountain Buddy Complete System..."
echo "================================================="

# Stop services first
echo "🛑 Stopping all services..."
launchctl stop "$MAIN_SERVICE" 2>/dev/null || true
launchctl stop "$BOT_SERVICE" 2>/dev/null || true

# Unload services
echo "📤 Unloading services..."
launchctl unload "$MAIN_PLIST" 2>/dev/null || true
launchctl unload "$BOT_PLIST" 2>/dev/null || true

# Disable auto-start
echo "⚡ Disabling auto-start..."
launchctl disable "gui/$(id -u)/$MAIN_SERVICE" 2>/dev/null || true
launchctl disable "gui/$(id -u)/$BOT_SERVICE" 2>/dev/null || true

# Remove plist files
echo "📋 Removing service configurations..."
[ -f "$MAIN_PLIST" ] && rm "$MAIN_PLIST"
[ -f "$BOT_PLIST" ] && rm "$BOT_PLIST"

echo ""
echo "✅ Fountain Buddy system completely uninstalled"
echo ""
echo "📂 Log files preserved in logs/ directory"
echo "   Remove manually if desired: rm -rf logs/"
echo ""
echo "🔧 To reinstall: ./service-install-all.sh"