#!/bin/bash
# View Fountain Buddy service logs

echo "🐦 Fountain Buddy Service Logs"
echo "==============================="

case "${1:-live}" in
    "live")
        echo "📺 Showing live logs (Ctrl+C to exit)..."
        echo ""
        if [ -f "logs/fountain-buddy.log" ]; then
            tail -f logs/fountain-buddy.log
        else
            echo "No log file found yet. Service may not have started."
        fi
        ;;
    
    "error" | "errors")
        echo "❌ Error logs:"
        echo ""
        if [ -f "logs/fountain-buddy-error.log" ]; then
            cat logs/fountain-buddy-error.log
        else
            echo "No error logs found."
        fi
        ;;
    
    "recent")
        echo "📋 Recent logs (last 50 lines):"
        echo ""
        if [ -f "logs/fountain-buddy.log" ]; then
            tail -50 logs/fountain-buddy.log
        else
            echo "No log file found."
        fi
        ;;
    
    "all")
        echo "📜 All logs:"
        echo ""
        if [ -f "logs/fountain-buddy.log" ]; then
            cat logs/fountain-buddy.log
        else
            echo "No log file found."
        fi
        ;;
    
    *)
        echo "Usage: $0 [live|error|recent|all]"
        echo ""
        echo "  live   - Show live logs (default)"
        echo "  error  - Show error logs"
        echo "  recent - Show last 50 lines" 
        echo "  all    - Show all logs"
        ;;
esac