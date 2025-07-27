#!/bin/bash
# Start Fountain Buddy service

SERVICE_NAME="com.fountainbuddy.service"
PLIST_PATH="$HOME/Library/LaunchAgents/com.fountainbuddy.service.plist"

echo "🚀 Starting Fountain Buddy service..."

if [ ! -f "$PLIST_PATH" ]; then
    echo "❌ Service not installed. Run ./service-install.sh first"
    exit 1
fi

# Start the service
launchctl start "$SERVICE_NAME"

sleep 2

# Check if it started
if launchctl list | grep -q "$SERVICE_NAME"; then
    echo "✅ Service started successfully"
    ./service-status.sh
else
    echo "❌ Failed to start service"
    exit 1
fi