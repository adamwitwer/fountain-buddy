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

### 🧠 Self-Training AI System
- **Continuous learning** - AI model improves from your corrections
- **Automated retraining** - Triggers when 15+ new identifications collected
- **Custom classifier** - Specialized for your backyard bird species
- **Transfer learning** - Fine-tuned ResNet-50 model for optimal accuracy
- **Quality control** - Uses only human-verified data for training

### 🔄 Complete Workflow
1. **Bird visits fountain** → Motion/AI detection triggers
2. **YOLO identifies bird** → Crops bird region from image
3. **AI species classification** → Custom model predicts species
4. **Discord notification** → Image + AI prediction + numbered species options sent
5. **Human verification** → Reply "3" for Blue Jay or type species name
6. **Automatic updates** → Database and filename updated with correct species
7. **Self-training** → AI model retrains nightly at 11:00 PM (when 15+ corrections collected)
8. **Daily reporting** → Email summary with accurate species data

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
   - AI prediction uses your custom-trained model for better accuracy

3. **Quick Response**
   - Reply with number: `4`
   - Or type species name: `Blue Jay`
   - Bot confirms: "✅ Thanks! Identified as **Blue Jay** (#4)"

4. **Automatic Updates**
   - Database updated with your identification
   - Image renamed: `bird_Blue_Jay_2025-07-01_14-30-15.jpg`
   - Training data collected for AI model improvement
   - Perfect accuracy for daily reports

### Daily Reports

Receive email summaries at 11 PM with:
- Total bird visits
- Species breakdown (your accurate data!)
- Sample images from the day

### AI Model Training

The system continuously learns from your corrections:
- **Daily auto-retraining** runs at 11:00 PM when 15+ new identifications collected
- **Automatic model reload** - service picks up new model without restart
- **Custom classifier** specialized for your specific bird species  
- **Quality control** ensures only human-verified data is used
- **Training logs** track model improvements over time
- **Fallback system** uses original classifier for low-confidence predictions

## 🏗️ Architecture

### Core Components

- **`run.py`** - Main application with camera monitoring and bird detection
- **`discord_bot.py`** - Bot for processing human identification responses
- **`bird_trainer.py`** - AI model training system with transfer learning
- **`auto_retrain.py`** - Automated retraining trigger system
- **`requirements.txt`** - Python dependencies
- **`.env.example`** - Configuration template

### Data Flow

```
**Real-time Detection & Verification:**
Camera Motion → YOLO Detection → AI Classification → Discord Alert
      ↓               ↓                ↓               ↓
   Image Saved → Bird Cropped → Species Predicted → Human Reply
      ↓               ↓                ↓               ↓  
Database Record ← File Renamed ← Verified Species ← Bot Processing
```

**Daily Automated Improvement (11:00 PM):**
```
Human Corrections → Training Check → Model Retraining → Auto Reload
       ↓                 ↓              ↓               ↓
   (15+ new) → Triggers Training → New Model File → Better AI
```

**Daily Reporting:**
```
Database Query → Species Summary → Email Report → Sent at 11:00 PM
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
├── bird_trainer.py        # AI model training system
├── auto_retrain.py        # Automated retraining trigger
├── requirements.txt       # Dependencies
├── .env.example          # Configuration template
├── .gitignore           # Git ignore rules
├── training_log.json     # Training session logs
├── models/               # Trained AI models
├── training_data/        # Organized training images
├── bird_images/          # All captured bird images
└── README.md            # This file
```

### Adding New Features

The modular design makes it easy to extend:
- **New detection methods** - Add to YOLO processing pipeline
- **Additional notifications** - Extend Discord webhook system
- **Enhanced AI models** - Modify training pipeline in `bird_trainer.py`
- **Data analysis** - Query SQLite database for insights
- **Multi-camera support** - Scale training data across multiple locations

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