# 🐦 Fountain Buddy

**Multi-camera AI-powered bird identification system with human-in-the-loop verification**  
**🚀 Optimized for Apple Silicon Macs (M1/M2/M3/M4) with 4x faster training**

Fountain Buddy is an intelligent bird monitoring system that combines computer vision, AI species classification, and human expertise to create the most accurate backyard bird identification system possible. Monitor multiple locations (fountain, peanut feeder, etc.) with separate cameras and unified AI classification.

## 🎯 **NEW: Mac M4 Pro Performance Breakthrough**
- **4x faster training**: 15 minutes vs 2+ hours on other platforms
- **Apple Silicon optimization**: TensorFlow Metal GPU acceleration


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

### 🧠 Custom CNN System
- **Custom CNN architecture** - Built from scratch specifically for bird classification
- **Clean NABirds foundation** - 1,596 balanced professional images (96-100 per species)
- **Hybrid enhancement** - Clean foundation + Discord corrections for continuous improvement
- **Apple Silicon optimized** - Custom training pipeline leverages M4 Pro Metal acceleration
- **Automated retraining** - Nightly improvements using clean base + human corrections


## 🚀 Installation

### Prerequisites
- **macOS 15.5+** with Apple Silicon (M1/M2/M3/M4) - *recommended for 4x faster training*
- **Python 3.12** (via Homebrew)
- **Xcode Command Line Tools**: `xcode-select --install`
- **Homebrew**: [Install here](https://brew.sh)
- One or more Reolink cameras with AI detection
- Discord server and bot token
- Email account (Gmail recommended)

### Quick Setup

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/fountain-buddy.git
   cd fountain-buddy
   
   # One-command setup (Mac with Apple Silicon optimization)
   ./setup-mac-py312.sh
   
   # Alternative: Manual setup for Linux/other systems
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-mac.txt  # Mac
   pip install -r requirements.txt      # Linux
   ```

   Tip: after running the setup script once, reuse the existing environment with:
   ```bash
   source venv/bin/activate
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your camera IPs, Discord tokens, etc.
   ```

3. **Test the system**
   ```bash
   source venv/bin/activate
   python run.py --init-db  # First time only
   
   # Test in two terminals:
   python run.py           # Terminal 1: Camera monitoring
   python discord_bot.py   # Terminal 2: Discord responses
   ```

4. **Keep it running**
   - Use two terminals or a process manager (launchd/systemd/pm2) to keep `run.py` and `discord_bot.py` running.
   - Service scripts are not included in this repo.

## 📦 Key Dependencies
- **TensorFlow 2.16+** - Deep learning framework (Metal GPU acceleration on Apple Silicon)
- **OpenCV** - Computer vision and image processing
- **Discord.py** - Bot integration for human feedback
- **Ultralytics** - YOLOv8 object detection
- **scikit-learn** - Data preprocessing and metrics
- **APScheduler** - Automated task scheduling

## ⚙️ Configuration

### Required Environment Variables

Create a `.env` file with the following settings:

```bash
# Multi-Camera Configuration (recommended)
# Camera 1 (e.g., fountain)
CAMERA1_IP=192.168.1.100
CAMERA1_USERNAME=your_camera_username
CAMERA1_PASSWORD=your_camera_password
CAMERA1_RTSP_PORT=554
CAMERA1_HTTP_PORT=80
CAMERA1_LOCATION=fountain

# Camera 2 (optional, e.g., peanut feeder)
CAMERA2_IP=192.168.1.101
CAMERA2_USERNAME=your_camera_username
CAMERA2_PASSWORD=your_camera_password
CAMERA2_RTSP_PORT=554
CAMERA2_HTTP_PORT=80
CAMERA2_LOCATION=peanut

# Email Configuration
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@gmail.com

# YOLO Configuration
YOLO_MODEL_PATH=yolov8n.pt
BIRD_CLASS_ID=14
CONFIDENCE_THRESHOLD=0.25
DETECTION_COOLDOWN_SECONDS=30

# File Configuration
IMAGE_DIR=bird_images

# AI Model Configuration
CUSTOM_MODEL_PATH=models/fountain_buddy_bird_classifier_unified.h5

# Discord Configuration
USE_DISCORD=true
DISCORD_BOT_TOKEN=your_bot_token

# Camera webhooks (used for sending detections)
DISCORD_WEBHOOK_CAMERA1=https://discord.com/api/webhooks/CAMERA1_WEBHOOK
DISCORD_WEBHOOK_CAMERA2=https://discord.com/api/webhooks/CAMERA2_WEBHOOK

# Discord Bot channel IDs (used for reading human responses)
DISCORD_CHANNEL_FOUNTAIN_ID=fountain_channel_id
DISCORD_CHANNEL_PEANUT_ID=peanut_channel_id
```

Notes:
- `camera_manager.py` supports both CAMERA1_/CAMERA2_ (recommended) and FOUNTAIN_/PEANUT_ variables for backward compatibility.
- The Discord bot listens on `DISCORD_CHANNEL_FOUNTAIN_ID` and `DISCORD_CHANNEL_PEANUT_ID`.

### Discord Setup

1. **Create Discord Application**
   - Go to https://discord.com/developers/applications
   - Create new application and bot
   - Enable "Message Content Intent"

2. **Set up Webhook**
   - Create separate webhooks in your two channels
   - Set `DISCORD_WEBHOOK_CAMERA1` and `DISCORD_WEBHOOK_CAMERA2` to those URLs

3. **Invite Bot**
   - Generate OAuth2 URL with "Send Messages" and "Read Message History" permissions
   - Invite bot to your server
   - Find your channel IDs and set `DISCORD_CHANNEL_FOUNTAIN_ID` and `DISCORD_CHANNEL_PEANUT_ID`

## 📱 Usage

### Workflow

1. **Motion/AI detection** triggers → **YOLO crops bird** → **Custom CNN predicts species**
2. **Discord notification** with image, AI prediction, and location-specific species options
3. **Human verification** via numbered reply or species name
4. **Automatic updates** to database, filename, and training data
5. **Nightly retraining** (11 PM) and daily email reports

### Daily Reports

Receive email summaries at 11 PM with:
- Total bird visits
- Species breakdown (your accurate data!)
- Sample images from the day

### AI Training Features
- **Apple Silicon acceleration** - 4x faster training with TensorFlow Metal
- **NABirds integration** - Professional dataset + your corrections for balanced training
- **Daily auto-retraining** - Runs at 11 PM when 15+ new identifications collected
- **Smart Sample Management** - Replaces weak NABirds samples with human corrections
- **Comprehensive evaluation** - Track accuracy improvements over time

## 📊 **NEW: Comprehensive Model Evaluation System**

Track real improvement with scientific rigor! Our advanced evaluation framework provides deep insights into model performance and improvement trends.

### 🎯 **What's Measured**

#### **📈 Training-Time Metrics**
- **Per-species validation accuracy** - See exactly which birds the model struggles with
- **Confidence calibration analysis** - Are 90% confident predictions actually right 90% of the time?
- **Learning curve progression** - Track improvements across epochs
- **Dataset quality metrics** - Monitor your human correction ratio improvements

#### **🌍 Real-World Performance Tracking**
- **Human correction rate** - Percentage of AI predictions that need correction
- **Species-specific field accuracy** - Blue Jays vs House Sparrows vs rare birds
- **Confidence calibration in production** - Real-world confidence vs actual accuracy
- **Time-series improvement analysis** - Track AI accuracy over weeks/months

#### **🏆 Dataset Quality Evolution**
- **Smart Sample Management tracking** - Monitor NABirds → Human sample replacement
- **Human correction distribution** - See which species benefit most from your expertise
- **Training data quality scores** - 🏆 >30% human, ⭐ >10% human indicators

### 🚀 **Enhanced Training Output**

Every training run now captures comprehensive metrics:

```
📊 Enhanced Dataset Summary:
  American Robin         : 150 (125N + 25H = 16.7% human) [CAPPED] ⭐
  Blue Jay              : 150 (135N + 15H = 10.0% human) [CAPPED] 
  House Sparrow         : 150 (120N + 30H = 20.0% human) [CAPPED] ⭐

🔍 Calculating per-species validation accuracy...
  American Robin        : 0.923 (35/38)
  Blue Jay             : 0.887 (31/35) 
  House Sparrow        : 0.756 (28/37)

📈 Analyzing confidence distribution...
  Very High confidence: 0.924 accuracy (156 samples)
  High confidence:     0.787 accuracy (89 samples)
  Medium confidence:   0.643 accuracy (67 samples)
```

### 📊 **Model Evaluation Dashboard**

Run comprehensive performance analysis anytime:

```bash
python3 model_evaluation_dashboard.py
```

**Sample Dashboard Output:**

```
🚀 FOUNTAIN BUDDY MODEL EVALUATION DASHBOARD
============================================================

📊 Overall Validation Accuracy Trend:
  🎯 2025-07-30 08:59: 0.279 (baseline)
  📈 2025-08-01 23:00: 0.324 (+0.045)
  📈 2025-08-05 23:00: 0.398 (+0.074)  ← Improving!

🐦 SPECIES-SPECIFIC PERFORMANCE ANALYSIS
  🥇 Blue Jay                 : 0.943 🔥 (35 validation samples)
  🥈 Northern Cardinal        : 0.887 ✅ (41 validation samples)  
  🥉 American Robin           : 0.823 ✅ (38 validation samples)
  ...
  ❌ House Finch              : 0.456 ❌ (12 validation samples)  ← Focus here!

🎯 CONFIDENCE CALIBRATION ANALYSIS
  🎯 Very High (90%+): 0.924 actual accuracy (156 samples)  ← Well calibrated!
  ⚠️ High (70%+):     0.634 actual accuracy (89 samples)   ← Overconfident

🌍 REAL-WORLD PERFORMANCE ANALYSIS (Last 30 Days)
Species                | Total | Corrections | AI Accuracy | Avg AI Conf
House Sparrow         |   145 |          23 |      84.1% ✅ |       0.72
European Starling     |   128 |          31 |      75.8% ✅ |       0.68
Blue Jay              |    47 |           2 |      95.7% 🔥 |       0.89  ← Excellent!

💡 Recommendations:
  🎉 Model is improving! Keep collecting corrections.
  📈 Focus corrections on species with <80% accuracy
  🎯 Aim for well-calibrated confidence (high confidence = high accuracy)
```

### ⚡ **Smart Sample Management Tracking**

Monitor how your corrections improve dataset quality:

```
🔄 House_Sparrow at cap (150/150)
   Replacing nabirds_old_image.jpg with human correction
🔄 European_Starling at cap (150/150)  
   Replacing nabirds_old_image.jpg with human correction

🏆 Dataset Quality Evolution:
  - Week 1: 5% human corrections average
  - Week 2: 12% human corrections average  ⭐
  - Week 3: 18% human corrections average  ⭐  
  - Week 4: 25% human corrections average  🏆
```

### 📅 **Recommended Evaluation Schedule**

- **After each training run** (every ~15 corrections) - See if latest corrections improved accuracy
- **Weekly spot checks** - Monitor real-world correction rates and focus areas  
- **Monthly deep dives** - Full trend analysis and calibration review

### 🎯 **Success Metrics to Track**

1. **Validation accuracy trending upward** ✅
2. **High-confidence predictions (>90%) accurate >90% of time** ✅  
3. **Species-specific accuracy improving for common birds** ✅
4. **Human correction rate decreasing over time** ✅
5. **Dataset quality indicators (🏆⭐) increasing** ✅

**Transform corrections into measurable AI improvement!** 🚀

## 🏗️ Architecture

### Core Components

#### 🔧 **Two-Service Architecture**
- **`run.py`** - 📹 Camera monitoring service (detects birds, sends alerts)
- **`discord_bot.py`** - 💬 Discord response service (processes human feedback)

#### 🧠 **Custom CNN Training System**
- **`train_clean_optimized_cnn.py`** - 🚀 **Working custom CNN trainer (64.6% accuracy)**
- **`bird_trainer_enhanced_cnn.py`** - 🎯 **Production trainer with Discord corrections integration**
- **`nabirds_clean_extractor.py`** - 🎯 **NABirds professional dataset extraction and curation**
- **`custom_bird_classifier.py`** - Enhanced classifier with automatic model selection
- **`auto_retrain.py`** - Automated retraining trigger system

#### 🛠 **Setup and Compatibility**
- **`setup-mac-py312.sh`** - One-command Mac setup with Apple Silicon optimization
- **`requirements-mac.txt`** - Mac-optimized dependencies with TensorFlow Metal support
- **`requirements.txt`** - Standard requirements
- **`.env.example`** - Configuration template

#### 🔧 **Core Infrastructure**
- **`camera_manager.py`** - Multi-camera management and location-aware processing
- **`photo_organizer.py`** - Location-aware photo organization


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
├── 🚀 CORE SERVICES
│   ├── run.py                         # Camera monitoring service
│   ├── discord_bot.py                 # Discord response service
│   ├── camera_manager.py              # Multi-camera management
│   └── photo_organizer.py             # Photo organization
│
├── 🧠 AI TRAINING
│   ├── bird_trainer_enhanced_cnn.py   # Apple Silicon optimized training
│   ├── model_evaluation_dashboard.py  # Performance analysis dashboard
│   ├── nabirds_clean_extractor.py     # NABirds dataset integration
│   ├── custom_bird_classifier.py      # Enhanced classifier
│   └── train_clean_optimized_cnn.py   # Base CNN trainer
│
├── 🛠 SETUP & CONFIG
│   ├── setup-mac-py312.sh            # One-command Mac setup
│   ├── requirements-mac.txt          # Mac-optimized dependencies
│   ├── requirements.txt              # Standard requirements
│   └── .env.example                  # Configuration template
│
├── 📊 DATA & MODELS
│   ├── models/                       # Trained AI models
│   ├── bird_images/active/           # Captured bird photos
│   ├── training_data_enhanced_cnn/   # Training dataset
│   ├── nabirds/                      # NABirds reference dataset
│   ├── logs/                         # Service logs
│   └── fountain_buddy.db             # SQLite database
│
└── 📚 DOCUMENTATION
    └── README.md                     # This file
```

### Extending the System
- **Additional cameras** - Add new locations to camera manager
- **New species** - Extend model with additional classes via NABirds integration
- **Enhanced AI models** - Modify training pipeline with Smart Sample Management
- **Data analysis** - Query SQLite database for insights
- **Performance tracking** - Extend evaluation dashboard with custom metrics

## 🙏 Acknowledgments

- **YOLO** - Object detection framework
- **Ultralytics** - YOLO implementation
- **Discord.py** - Discord bot framework
- **TensorFlow** - AI/ML framework
- **Reolink** - Camera integration

---

**Built with ❤️ for bird enthusiasts and AI developers**

*Transform your backyard into an intelligent bird research station!* 🐦🤖📊