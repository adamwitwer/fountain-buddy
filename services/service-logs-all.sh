#!/bin/bash
# View logs from both Fountain Buddy services

echo "🐦 Fountain Buddy Complete System Logs"
echo "======================================"

case "${1:-recent}" in
    "live")
        echo "📺 Showing live logs from both services..."
        echo "Press Ctrl+C to exit"
        echo ""
        echo "🟢 Camera logs will be prefixed with [CAMERA]"
        echo "🔵 Discord logs will be prefixed with [DISCORD]"
        echo ""
        
        # Use multitail if available, otherwise fallback to tail
        if command -v multitail >/dev/null 2>&1; then
            multitail \
                -i logs/fountain-buddy.log \
                -i logs/discord-bot.log
        else
            # Fallback: tail both files with prefixes
            (tail -f logs/fountain-buddy.log 2>/dev/null | sed 's/^/[CAMERA] /' &) 
            (tail -f logs/discord-bot.log 2>/dev/null | sed 's/^/[DISCORD] /' &)
            wait
        fi
        ;;
    
    "camera")
        echo "📹 Camera monitoring logs:"
        echo ""
        if [ -f "logs/fountain-buddy.log" ]; then
            tail -50 logs/fountain-buddy.log
        else
            echo "No camera logs found."
        fi
        ;;
    
    "discord" | "bot")
        echo "💬 Discord bot logs:"
        echo ""
        if [ -f "logs/discord-bot.log" ]; then
            tail -50 logs/discord-bot.log
        else
            echo "No Discord bot logs found."
        fi
        ;;
    
    "error" | "errors")
        echo "❌ Error logs:"
        echo ""
        echo "🔴 Camera errors:"
        if [ -f "logs/fountain-buddy-error.log" ]; then
            cat logs/fountain-buddy-error.log
        else
            echo "No camera error logs."
        fi
        
        echo ""
        echo "🔴 Discord bot errors:"
        if [ -f "logs/discord-bot-error.log" ]; then
            cat logs/discord-bot-error.log
        else
            echo "No Discord bot error logs."
        fi
        ;;
    
    "recent")
        echo "📋 Recent logs (last 20 lines each):"
        echo ""
        echo "🟢 Camera Monitor:"
        echo "$(printf '%.50s' "--------------------------------------------------")"
        if [ -f "logs/fountain-buddy.log" ]; then
            tail -20 logs/fountain-buddy.log
        else
            echo "No camera logs found."
        fi
        
        echo ""
        echo "🔵 Discord Bot:"
        echo "$(printf '%.50s' "--------------------------------------------------")"
        if [ -f "logs/discord-bot.log" ]; then
            tail -20 logs/discord-bot.log
        else
            echo "No Discord bot logs found."
        fi
        ;;
    
    *)
        echo "Usage: $0 [recent|live|camera|discord|error]"
        echo ""
        echo "  recent  - Recent logs from both services (default)"
        echo "  live    - Live logs from both services"
        echo "  camera  - Camera monitoring logs only"
        echo "  discord - Discord bot logs only"
        echo "  error   - Error logs from both services"
        echo ""
        echo "Individual log files:"
        echo "  Camera:  logs/fountain-buddy.log"
        echo "  Discord: logs/discord-bot.log"
        ;;
esac