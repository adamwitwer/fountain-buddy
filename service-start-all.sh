#!/bin/bash
# Start both Fountain Buddy services

MAIN_SERVICE="com.fountainbuddy.service"
BOT_SERVICE="com.fountainbuddy.discordbot"

echo "🚀 Starting Fountain Buddy Complete System..."

# Check if services are installed
if [ ! -f "$HOME/Library/LaunchAgents/com.fountainbuddy.service.plist" ]; then
    echo "❌ Services not installed. Run ./service-install-all.sh first"
    exit 1
fi

# Start camera monitoring service
echo "📹 Starting camera monitoring service..."
launchctl start "$MAIN_SERVICE"

# Start Discord bot service
echo "💬 Starting Discord bot service..."
launchctl start "$BOT_SERVICE"

sleep 3

echo ""
echo "✅ Services started!"
echo ""

# Show status
./service-status-all.sh