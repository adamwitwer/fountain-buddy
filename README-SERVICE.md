# 🐦 Fountain Buddy macOS Service Setup

## Quick Start - Complete System

```bash
# Install both services (camera + Discord bot)
./service-install-all.sh

# Check system status
./service-status-all.sh

# View live logs from both services
./service-logs-all.sh
```

## 🔧 Two-Service Architecture

Fountain Buddy runs as **two separate services**:

1. **📹 Camera Monitor** (`fountain-buddy`) - Detects birds, takes photos
2. **💬 Discord Bot** (`discord-bot`) - Handles human feedback loop

Both services work together but run independently for reliability.

## Service Management Commands

| Command | Description |
|---------|-------------|
| `./service-install.sh` | Install service (auto-starts at login) |
| `./service-start.sh` | Start the service |
| `./service-stop.sh` | Stop the service |
| `./service-status.sh` | Check service status |
| `./service-logs.sh` | View live logs |
| `./service-logs.sh error` | View error logs |
| `./service-uninstall.sh` | Remove service completely |

## Service Features

✅ **Auto-start at login** - Runs automatically when you log in  
✅ **Auto-restart on crash** - Restarts if the app crashes  
✅ **Proper logging** - Logs to `logs/fountain-buddy.log`  
✅ **Error handling** - Errors logged to `logs/fountain-buddy-error.log`  
✅ **Background process** - Runs silently in background  

## Log Files

- **Main logs**: `logs/fountain-buddy.log`
- **Error logs**: `logs/fountain-buddy-error.log`

## Troubleshooting

### Service won't start
```bash
# Check logs for errors
./service-logs.sh error

# Manually test the app
source venv/bin/activate
python run.py
```

### Permission issues
```bash
# Fix permissions
chmod +x service-*.sh
```

### View system logs
```bash
# Check macOS system logs
log show --predicate 'subsystem == "com.apple.launchd"' --last 1h
```

## Configuration

The service uses the same `.env` file as manual runs. Make sure your:
- Camera settings are correct
- Discord bot is configured  
- All credentials are set

## How it Works

The service uses **launchd** (macOS's built-in service manager):

1. **Plist file** defines the service configuration
2. **LaunchAgents** directory contains user-level services
3. **KeepAlive** ensures the service restarts on crashes
4. **RunAtLoad** starts the service at login
5. **Logging** redirects output to log files

This is the macOS equivalent of systemd on Linux!

## Manual Commands (if needed)

```bash
# Manual launchctl commands
launchctl load ~/Library/LaunchAgents/com.fountainbuddy.service.plist
launchctl start com.fountainbuddy.service
launchctl stop com.fountainbuddy.service
launchctl unload ~/Library/LaunchAgents/com.fountainbuddy.service.plist
```