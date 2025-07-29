#!/bin/bash
# Check Fountain Buddy service status

SERVICE_NAME="com.fountainbuddy.service"

echo "🐦 Fountain Buddy Service Status"
echo "================================"

# Check if service is loaded
if launchctl list | grep -q "$SERVICE_NAME"; then
    echo "✅ Service is loaded"
    
    # Get detailed status
    STATUS=$(launchctl list "$SERVICE_NAME" 2>/dev/null)
    
    if echo "$STATUS" | grep -q '"PID" = [0-9]'; then
        PID=$(echo "$STATUS" | grep '"PID"' | sed 's/.*= \([0-9]*\).*/\1/')
        echo "✅ Service is running (PID: $PID)"
    else
        echo "⚠️ Service is loaded but not running"
    fi
    
    # Show last exit status if available
    if echo "$STATUS" | grep -q '"LastExitStatus"'; then
        EXIT_STATUS=$(echo "$STATUS" | grep '"LastExitStatus"' | sed 's/.*= \([0-9]*\).*/\1/')
        if [ "$EXIT_STATUS" = "0" ]; then
            echo "✅ Last exit: Success (0)"
        else
            echo "❌ Last exit: Error ($EXIT_STATUS)"
        fi
    fi
    
else
    echo "❌ Service is not loaded"
fi

echo ""
echo "Recent logs (last 10 lines):"
echo "============================="
if [ -f "logs/fountain-buddy.log" ]; then
    tail -10 logs/fountain-buddy.log
else
    echo "No logs found"
fi

echo ""
echo "Commands:"
echo "  View live logs: tail -f logs/fountain-buddy.log"
echo "  View errors:    tail -f logs/fountain-buddy-error.log"