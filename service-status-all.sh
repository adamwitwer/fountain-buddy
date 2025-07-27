#!/bin/bash
# Check status of both Fountain Buddy services

MAIN_SERVICE="com.fountainbuddy.service"
BOT_SERVICE="com.fountainbuddy.discordbot"

echo "🐦 Fountain Buddy Complete System Status"
echo "========================================"

# Function to check a service
check_service() {
    local service_name=$1
    local display_name=$2
    
    echo ""
    echo "🔧 $display_name"
    echo "$(printf '%.40s' "----------------------------------------")"
    
    if launchctl list | grep -q "$service_name"; then
        echo "✅ Service is loaded"
        
        STATUS=$(launchctl list "$service_name" 2>/dev/null)
        
        if echo "$STATUS" | grep -q '"PID" = [0-9]'; then
            PID=$(echo "$STATUS" | grep '"PID"' | sed 's/.*= \([0-9]*\).*/\1/')
            echo "✅ Running (PID: $PID)"
        else
            echo "⚠️ Loaded but not running"
        fi
        
        if echo "$STATUS" | grep -q '"LastExitStatus"'; then
            EXIT_STATUS=$(echo "$STATUS" | grep '"LastExitStatus"' | sed 's/.*= \([0-9]*\).*/\1/')
            if [ "$EXIT_STATUS" = "0" ]; then
                echo "✅ Last exit: Success (0)"
            else
                echo "❌ Last exit: Error ($EXIT_STATUS)"
            fi
        fi
    else
        echo "❌ Service not loaded"
    fi
}

# Check both services
check_service "$MAIN_SERVICE" "Camera Monitor Service"
check_service "$BOT_SERVICE" "Discord Bot Service"

echo ""
echo "📊 System Overview"
echo "=================="

# Count running services
RUNNING_COUNT=0
if launchctl list | grep -q "$MAIN_SERVICE" && launchctl list "$MAIN_SERVICE" 2>/dev/null | grep -q '"PID" = [0-9]'; then
    ((RUNNING_COUNT++))
fi
if launchctl list | grep -q "$BOT_SERVICE" && launchctl list "$BOT_SERVICE" 2>/dev/null | grep -q '"PID" = [0-9]'; then
    ((RUNNING_COUNT++))
fi

echo "Services running: $RUNNING_COUNT/2"

if [ "$RUNNING_COUNT" = "2" ]; then
    echo "🎉 Complete system operational!"
elif [ "$RUNNING_COUNT" = "1" ]; then
    echo "⚠️ Partial system running"
else
    echo "❌ System not running"
fi

echo ""
echo "📋 Quick Commands:"
echo "  Recent camera logs:  tail -20 logs/fountain-buddy.log"
echo "  Recent Discord logs: tail -20 logs/discord-bot.log"
echo "  Live camera logs:    tail -f logs/fountain-buddy.log"
echo "  Live Discord logs:   tail -f logs/discord-bot.log"