#!/bin/bash
# Stop Fountain Buddy service

SERVICE_NAME="com.fountainbuddy.service"

echo "🛑 Stopping Fountain Buddy service..."

# Stop the service
launchctl stop "$SERVICE_NAME"

sleep 2

# Check if it stopped
if launchctl list | grep -q "$SERVICE_NAME"; then
    STATUS=$(launchctl list "$SERVICE_NAME" 2>/dev/null)
    if echo "$STATUS" | grep -q '"PID" = [0-9]'; then
        echo "⚠️ Service still running, force stopping..."
        launchctl kill TERM "gui/501/$SERVICE_NAME"
        sleep 2
    fi
fi

echo "✅ Service stopped"