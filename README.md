# 🐦 Fountain Buddy

**Multi-camera AI-powered bird identification system with human-in-the-loop verification**

Fountain Buddy is an intelligent bird monitoring system that combines computer vision, AI species classification, and human expertise to create the most accurate backyard bird identification system possible. Monitor multiple locations (fountain, peanut feeder, etc.) with separate cameras and unified AI classification.

## ✨ Features

### 🤖 AI-Powered Detection
- **Multi-camera support** - Monitor fountain, peanut feeder, and other locations simultaneously
- **YOLO bird detection** - Never miss a bird visitor at any location
- **Motion/AI triggers** - Efficient monitoring with Reolink camera integration
- **Automatic image capture** - High-quality photos of every bird with location tracking

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
- **Unified 19-class model** - Single classifier for all locations (fountain + peanut species)
- **Continuous learning** - AI model improves from your corrections across all cameras
- **Automated retraining** - Triggers when 15+ new identifications collected
- **Cross-location learning** - European Starling data from multiple feeders improves accuracy
- **Transfer learning** - Fine-tuned ResNet-50 model for optimal accuracy
- **Quality control** - Uses only human-verified data for training

### 🔄 Complete Workflow
1. **Bird visits location** → Motion/AI detection triggers at fountain, peanut feeder, etc.
2. **YOLO identifies bird** → Crops bird region from image
3. **AI species classification** → Unified 19-class model predicts species
4. **Location-aware Discord notification** → Image + AI prediction + location-specific species options
5. **Human verification** → Reply "3" for Blue Jay or type species name
6. **Automatic updates** → Database and filename updated with correct species and location
7. **Cross-location training** → AI model retrains nightly at 11:00 PM using data from all cameras
8. **Daily reporting** → Email summary with accurate species data by location

## 🚀 Installation

### Prerequisites
- Python 3.8+
- One or more Reolink cameras with AI detection
- Discord server and bot token
- Email account (Gmail recommended)
- Separate Discord channels for each camera location (optional but recommended)

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
# Multi-Camera Configuration
# Camera 1 - Fountain
FOUNTAIN_CAMERA_IP=192.168.1.100
FOUNTAIN_USERNAME=your_camera_username
FOUNTAIN_PASSWORD=your_camera_password
FOUNTAIN_RTSP_PORT=554
FOUNTAIN_HTTP_PORT=80

# Camera 2 - Peanut Feeder (optional)
PEANUT_CAMERA_IP=192.168.1.101
PEANUT_USERNAME=your_camera_username
PEANUT_PASSWORD=your_camera_password
PEANUT_RTSP_PORT=554
PEANUT_HTTP_PORT=80

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
DISCORD_BOT_TOKEN=your_bot_token

# Fountain Camera Discord
DISCORD_WEBHOOK_FOUNTAIN=https://discord.com/api/webhooks/FOUNTAIN_WEBHOOK
DISCORD_CHANNEL_FOUNTAIN_ID=fountain_channel_id

# Peanut Camera Discord (optional)
DISCORD_WEBHOOK_PEANUT=https://discord.com/api/webhooks/PEANUT_WEBHOOK
DISCORD_CHANNEL_PEANUT_ID=peanut_channel_id
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

2. **Location-Aware Discord Notification**
   - Receive message like:
     ```
     🐦 New bird at fountain! YOLO confidence: 0.85
     🤖 AI thinks: Blue Jay (0.73)
     
     What species is this? Reply with number:
     1. Northern Cardinal
     2. American Robin
     3. Common Grackle
     4. Blue Jay
     5. Mourning Dove
     ...
     
     📍 Location: Fountain
     ```
   - Different species options for each camera location
   - AI prediction uses unified 19-class model for better accuracy

3. **Quick Response**
   - Reply with number: `4`
   - Or type species name: `Blue Jay`
   - Bot confirms: "✅ Thanks! Identified as **Blue Jay** (#4)"

4. **Automatic Updates**
   - Database updated with your identification and location
   - Image saved to location folder: `bird_images/fountain/bird_Blue_Jay_2025-07-01_14-30-15.jpg`
   - Training data collected for unified AI model improvement
   - Perfect accuracy for daily reports by location

### Daily Reports

Receive email summaries at 11 PM with:
- Total bird visits
- Species breakdown (your accurate data!)
- Sample images from the day

### AI Model Training

The system continuously learns from your corrections across all camera locations:
- **Unified 19-class model** covers fountain birds + peanut feeder species
- **Cross-location learning** - European Starling data from multiple cameras improves accuracy
- **Daily auto-retraining** runs at 11:00 PM when 15+ new identifications collected
- **Automatic model reload** - service picks up new model without restart
- **Multi-location training data** from fountain, peanut feeder, and future cameras
- **Quality control** ensures only human-verified data is used
- **Training logs** track model improvements over time
- **Fallback system** uses legacy model for species without sufficient training data

## 🏗️ Architecture

### Core Components

- **`run.py`** - Main application with multi-camera monitoring and bird detection
- **`camera_manager.py`** - Multi-camera management and location-aware processing
- **`discord_bot.py`** - Bot for processing human identification responses
- **`bird_trainer_unified.py`** - Unified 19-class AI model training system
- **`custom_bird_classifier.py`** - Enhanced classifier with unified model support
- **`species_mapping.py`** - Species classification and location mapping
- **`photo_organizer.py`** - Location-aware photo organization
- **`auto_retrain.py`** - Automated retraining trigger system
- **`requirements.txt`** - Python dependencies
- **`.env.example`** - Configuration template

### Data Flow

```
**Multi-Camera Real-time Detection & Verification:**
Multi-Camera Motion → YOLO Detection → Unified AI Model → Location-Aware Discord Alert
        ↓                   ↓              ↓                        ↓
   Location-Tagged → Bird Cropped → 19-Class Prediction → Location-Specific Options
     Image Saved         ↓              ↓                        ↓  
   Database Record ← Location Folder ← Verified Species ← Bot Processing
```

**Daily Automated Improvement (11:00 PM):**
```
Multi-Location Corrections → Training Check → Unified Model Retraining → Auto Reload
          ↓                      ↓                    ↓                    ↓
   (15+ cross-location) → Triggers Training → New 19-Class Model → Better AI
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
    image_path TEXT,
    location TEXT,          -- Camera location (fountain/peanut/etc)
    camera_id TEXT          -- Camera identifier
);
```

## 🛠️ Development

### Project Structure
```
fountain-buddy/
├── run.py                    # Main multi-camera application
├── camera_manager.py         # Multi-camera management
├── discord_bot.py            # Discord bot for human feedback
├── bird_trainer_unified.py   # Unified 19-class AI training
├── custom_bird_classifier.py # Enhanced classifier
├── species_mapping.py        # Species classification system
├── photo_organizer.py        # Location-aware photo organization
├── photo_cleanup_scheduler.py # Automated photo cleanup
├── prepare_training_data.py  # Training data preparation
├── auto_retrain.py           # Automated retraining trigger
├── requirements.txt          # Dependencies
├── .env.example             # Configuration template
├── .gitignore              # Git ignore rules
├── models/                  # Trained AI models
├── training_data_unified/   # 19-class training structure
├── bird_images/            # Location-organized bird images
│   ├── fountain/           # Fountain camera images
│   ├── peanut/            # Peanut feeder camera images
│   └── archive/           # Archived images
├── memory-bank/            # Project documentation
│   ├── project-overview.md
│   ├── multi-camera-plan.md
│   └── ai-model-expansion.md
└── README.md              # This file
```

### Adding New Features

The modular design makes it easy to extend:
- **Additional cameras** - Add new locations to camera manager
- **New detection methods** - Add to YOLO processing pipeline
- **Additional notifications** - Extend Discord webhook system
- **Enhanced AI models** - Modify unified training pipeline
- **New species** - Extend 19-class model with additional classes
- **Data analysis** - Query SQLite database for location-based insights
- **Custom locations** - Support any number of camera locations

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