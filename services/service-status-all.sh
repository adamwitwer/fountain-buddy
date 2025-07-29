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
    
    # Check if service is loaded and get PID from launchctl list
    LIST_OUTPUT=$(launchctl list | grep "$service_name")
    
    if [ -n "$LIST_OUTPUT" ]; then
        echo "✅ Service is loaded"
        
        # Parse PID from launchctl list output: "PID STATUS SERVICE_NAME"
        PID=$(echo "$LIST_OUTPUT" | awk '{print $1}')
        
        if [ "$PID" != "-" ] && [ -n "$PID" ]; then
            echo "✅ Running (PID: $PID)"
            RUNNING=true
        else
            echo "⚠️ Loaded but not running"
            RUNNING=false
        fi
        
        # Get last exit status from detailed output
        DETAILED_STATUS=$(launchctl list "$service_name" 2>/dev/null)
        if echo "$DETAILED_STATUS" | grep -q '"LastExitStatus"'; then
            EXIT_STATUS=$(echo "$DETAILED_STATUS" | grep '"LastExitStatus"' | sed 's/.*= \([0-9]*\).*/\1/')
            if [ "$EXIT_STATUS" = "0" ]; then
                echo "✅ Last exit: Success (0)"
            else
                echo "❌ Last exit: Error ($EXIT_STATUS)"
            fi
        fi
    else
        echo "❌ Service not loaded"
        RUNNING=false
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

# Check main service
MAIN_LIST=$(launchctl list | grep "$MAIN_SERVICE")
if [ -n "$MAIN_LIST" ]; then
    MAIN_PID=$(echo "$MAIN_LIST" | awk '{print $1}')
    if [ "$MAIN_PID" != "-" ] && [ -n "$MAIN_PID" ]; then
        ((RUNNING_COUNT++))
    fi
fi

# Check bot service
BOT_LIST=$(launchctl list | grep "$BOT_SERVICE")
if [ -n "$BOT_LIST" ]; then
    BOT_PID=$(echo "$BOT_LIST" | awk '{print $1}')
    if [ "$BOT_PID" != "-" ] && [ -n "$BOT_PID" ]; then
        ((RUNNING_COUNT++))
    fi
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