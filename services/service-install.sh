#!/bin/bash
# Install Fountain Buddy as a macOS launchd service

set -e

PROJECT_DIR="/Users/adam/Documents/Projects/fountain-buddy"
PLIST_FILE="com.fountainbuddy.service.plist"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
SERVICE_NAME="com.fountainbuddy.service"

echo "🐦 Installing Fountain Buddy Service..."

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCHD_DIR"

# Copy plist file to LaunchAgents
echo "📋 Installing service configuration..."
cp "$PROJECT_DIR/$PLIST_FILE" "$LAUNCHD_DIR/"

# Load the service
echo "🚀 Loading service..."
launchctl load "$LAUNCHD_DIR/$PLIST_FILE"

# Enable the service to start at login
echo "⚡ Enabling auto-start..."
launchctl enable "gui/$(id -u)/$SERVICE_NAME"

echo "✅ Fountain Buddy service installed successfully!"
echo ""
echo "Service Management:"
echo "  Status:    ./service-status.sh"
echo "  Stop:      ./service-stop.sh"
echo "  Start:     ./service-start.sh"
echo "  Logs:      ./service-logs.sh"
echo "  Uninstall: ./service-uninstall.sh"
echo ""
echo "Logs will be written to:"
echo "  Output: logs/fountain-buddy.log"
echo "  Errors: logs/fountain-buddy-error.log"