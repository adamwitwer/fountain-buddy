# 🐦 Fountain Buddy

**AI-powered bird identification system with human-in-the-loop verification**

Fountain Buddy is an intelligent bird monitoring system that combines computer vision, AI species classification, and human expertise to create the most accurate backyard bird identification system possible.

## ✨ Features

### 🤖 AI-Powered Detection
- **YOLO bird detection** - Never miss a bird visitor
- **Motion/AI triggers** - Efficient monitoring with Reolink camera integration
- **Automatic image capture** - High-quality photos of every bird

### 🎯 Human-in-the-Loop Verification
- **Discord notifications** - Real-time alerts with bird images
- **Numbered species options** - Quick identification with simple replies
- **Expert verification** - Your bird knowledge beats any AI
- **Instant feedback** - Database updates and file renaming in real-time

### 📊 Smart Data Management
- **SQLite database** - Permanent record of all bird visits
- **Intelligent file naming** - Images organized by species and timestamp
- **Daily email summaries** - Beautiful reports with accurate species counts
- **Confidence tracking** - AI vs human identification comparison

### 🔄 Complete Workflow
1. **Bird visits fountain** → Motion/AI detection triggers
2. **YOLO identifies bird** → Crops bird region from image
3. **Discord notification** → Image + numbered species options sent
4. **Human verification** → Reply "3" for Blue Jay or type species name
5. **Automatic updates** → Database and filename updated with correct species
6. **Daily reporting** → Email summary with accurate species data

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Reolink camera with AI detection
- Discord server and bot token
- Email account (Gmail recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fountain-buddy.git
   cd fountain-buddy
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings (see Configuration section)
   ```

5. **Initialize database**
   ```bash
   python3 run.py --init-db
   ```

## ⚙️ Configuration

### Required Environment Variables

Create a `.env` file with the following settings:

```bash
# Camera Configuration
CAMERA_IP=192.168.1.100
USERNAME=your_camera_username
PASSWORD=your_camera_password
RTSP_PORT=554
HTTP_PORT=80
BASE_URL=http://192.168.1.100:80/cgi-bin/api.cgi

# Email Configuration
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@gmail.com

# YOLO Configuration
YOLO_MODEL_PATH=yolov8n.pt
BIRD_CLASS_ID=14
CONFIDENCE_THRESHOLD=0.25
DETECTION_COOLDOWN_SECONDS=30

# Discord Configuration
USE_DISCORD=true
DISCORD_WEBHOOK_PROD=https://discord.com/api/webhooks/YOUR_WEBHOOK
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id
```

### Discord Setup

1. **Create Discord Application**
   - Go to https://discord.com/developers/applications
   - Create new application and bot
   - Enable "Message Content Intent"

2. **Set up Webhook**
   - Create webhook in your Discord channel
   - Copy webhook URL to `DISCORD_WEBHOOK_PROD`

3. **Invite Bot**
   - Generate OAuth2 URL with "Send Messages" and "Read Message History" permissions
   - Invite bot to your server

## 📱 Usage

### Bird Identification Workflow

1. **Automatic Detection**
   - System monitors camera for motion/AI triggers
   - YOLO detects and crops birds from images

2. **Discord Notification**
   - Receive message like:
     ```
     🐦 New bird detected! YOLO confidence: 0.85
     🤖 AI thinks: Blue Jay (0.73)
     
     What species is this? Reply with number:
     1. Northern Cardinal
     2. American Robin
     3. Common Grackle
     4. Blue Jay
     5. Mourning Dove
     ...
     ```

3. **Quick Response**
   - Reply with number: `4`
   - Or type species name: `Blue Jay`
   - Bot confirms: "✅ Thanks! Identified as **Blue Jay** (#4)"

4. **Automatic Updates**
   - Database updated with your identification
   - Image renamed: `bird_Blue_Jay_2025-07-01_14-30-15.jpg`
   - Perfect accuracy for daily reports

### Daily Reports

Receive email summaries at 11 PM with:
- Total bird visits
- Species breakdown (your accurate data!)
- Sample images from the day

## 🏗️ Architecture

### Core Components

- **`run.py`** - Main application with camera monitoring and bird detection
- **`discord_bot.py`** - Bot for processing human identification responses
- **`requirements.txt`** - Python dependencies
- **`.env.example`** - Configuration template

### Data Flow

```
Camera → Motion Detection → YOLO → Species Crop → Discord Notification
                                                          ↓
Database ← File Rename ← Human Response ← Discord Bot ← Human Reply
                                                          ↓
Daily Email ← Species Summary ← Database Query ← Scheduled Task
```

### Database Schema

```sql
CREATE TABLE bird_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    bird_type TEXT NOT NULL,
    species TEXT,           -- Human-verified species
    confidence REAL,        -- Confidence score (1.0 for human)
    image_path TEXT
);
```

## 🛠️ Development

### Project Structure
```
fountain-buddy/
├── run.py                 # Main application
├── discord_bot.py         # Discord bot for human feedback
├── requirements.txt       # Dependencies
├── .env.example          # Configuration template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

### Adding New Features

The modular design makes it easy to extend:
- **New detection methods** - Add to YOLO processing pipeline
- **Additional notifications** - Extend Discord webhook system
- **Enhanced AI models** - Integrate new species classifiers
- **Data analysis** - Query SQLite database for insights

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **YOLO** - Object detection framework
- **Ultralytics** - YOLO implementation
- **Discord.py** - Discord bot framework
- **TensorFlow** - AI/ML framework
- **Reolink** - Camera integration

---

**Built with ❤️ for bird enthusiasts and AI developers**

*Transform your backyard into an intelligent bird research station!* 🐦🤖📊