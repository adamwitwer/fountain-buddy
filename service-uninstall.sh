#!/bin/bash
# Uninstall Fountain Buddy service

SERVICE_NAME="com.fountainbuddy.service"
PLIST_PATH="$HOME/Library/LaunchAgents/com.fountainbuddy.service.plist"

echo "🗑️ Uninstalling Fountain Buddy service..."

# Stop the service first
echo "🛑 Stopping service..."
launchctl stop "$SERVICE_NAME" 2>/dev/null || true

# Unload the service
echo "📤 Unloading service..."
launchctl unload "$PLIST_PATH" 2>/dev/null || true

# Disable auto-start
echo "⚡ Disabling auto-start..."
launchctl disable "gui/$(id -u)/$SERVICE_NAME" 2>/dev/null || true

# Remove the plist file
if [ -f "$PLIST_PATH" ]; then
    echo "📋 Removing service configuration..."
    rm "$PLIST_PATH"
fi

echo "✅ Fountain Buddy service uninstalled"
echo ""
echo "Note: Log files in logs/ directory were preserved"
echo "Remove them manually if desired: rm -rf logs/"