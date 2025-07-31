#!/bin/bash
# Stop both Fountain Buddy services

MAIN_SERVICE="com.fountainbuddy.service"
BOT_SERVICE="com.fountainbuddy.discordbot"

echo "🛑 Stopping Fountain Buddy Complete System..."

# Stop camera monitoring service
echo "📹 Stopping camera monitoring service..."
launchctl stop "$MAIN_SERVICE"

# Stop Discord bot service
echo "💬 Stopping Discord bot service..."
launchctl stop "$BOT_SERVICE"

sleep 3

# Force stop if needed
echo "🔍 Checking if services stopped..."

for service in "$MAIN_SERVICE" "$BOT_SERVICE"; do
    if launchctl list | grep -q "$service"; then
        STATUS=$(launchctl list "$service" 2>/dev/null)
        if echo "$STATUS" | grep -q '"PID" = [0-9]'; then
            echo "⚠️ Force stopping $service..."
            launchctl kill TERM "gui/501/$service"
        fi
    fi
done

sleep 2

echo ""
echo "✅ All services stopped!"