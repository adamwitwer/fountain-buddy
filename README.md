# 🐦 Fountain Buddy

**Multi-camera AI-powered bird identification system with human-in-the-loop verification**  
**🚀 Optimized for Apple Silicon Macs (M1/M2/M3/M4) with 4x faster training**

Fountain Buddy is an intelligent bird monitoring system that combines computer vision, AI species classification, and human expertise to create the most accurate backyard bird identification system possible. Monitor multiple locations (fountain, peanut feeder, etc.) with separate cameras and unified AI classification.

## 🎯 **NEW: Mac M4 Pro Performance Breakthrough**
- **4x faster training**: 15 minutes vs 2+ hours on other platforms
- **Apple Silicon optimization**: TensorFlow Metal GPU acceleration
- **Seamless service management**: Native macOS launchd integration
- **Production ready**: Auto-start, auto-restart, comprehensive logging

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

### 🧠 Enhanced Self-Training AI System
- **NABirds-boosted training** - Professional dataset with 265+ additional images for balanced training
- **Hybrid training data** - Combines your human-verified local data with high-quality NABirds professional images
- **Dramatically improved accuracy** - Blue Jay samples boosted from 8 to 80 (+900% improvement)
- **Balanced dataset** - All species now have 80-120 training samples for consistent performance
- **Optimized training pipeline** - Mixed precision, enhanced augmentation, learning rate scheduling
- **3-5x faster training** - Advanced optimizations reduce training time from hours to minutes
- **Automated retraining** - Triggers when 15+ new identifications collected, now using enhanced pipeline
- **Transfer learning** - Fine-tuned ResNet-50 with ImageNet initialization for optimal accuracy
- **Quality control** - Uses only human-verified data combined with curated professional images

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

### 🎯 **Recommended: Mac M4 Pro Setup (Fastest)**

#### Prerequisites
- **macOS 15.5+** with Apple Silicon (M1/M2/M3/M4)
- **Python 3.12** (via Homebrew)
- **Xcode Command Line Tools**: `xcode-select --install`
- **Homebrew**: [Install here](https://brew.sh)
- One or more Reolink cameras with AI detection
- Discord server and bot token
- Email account (Gmail recommended)

#### Quick Setup

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/fountain-buddy.git
   cd fountain-buddy
   
   # Check compatibility
   python3 check_compatibility.py
   
   # One-command setup (uses Python 3.12 + Apple Silicon optimization)
   ./setup-mac-py312.sh
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

4. **Install as permanent services**
   ```bash
   # Install both camera monitor + Discord bot as background services
   ./service-install-all.sh
   
   # Check status
   ./service-status-all.sh
   
   # View live logs
   ./service-logs-all.sh
   ```

✅ **Services auto-start at login and restart on crashes!**

### 🐧 **Alternative: Linux/WSL2 Setup** 

For non-Mac systems (performance will be slower):

1. **Standard setup**
   ```bash
   git clone https://github.com/yourusername/fountain-buddy.git
   cd fountain-buddy
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure and run**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
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

### Enhanced AI Model Training

The system features a revolutionary training approach optimized for Apple Silicon performance:

#### 🚀 **Apple Silicon Acceleration**
- **Mac M4 Pro**: 15 minutes training time (vs 2+ hours on other platforms)
- **TensorFlow Metal**: Native GPU acceleration for Apple Silicon
- **Unified memory**: Efficient data loading and processing
- **Real-time feedback**: Fast iteration cycle for model improvements

#### 🎯 **NABirds Integration**
- **Professional dataset boost** - 265+ curated NABirds images added for balanced training
- **Massive accuracy improvements** - Blue Jay samples: 8 → 80 (+900%), Gray Catbird: 30 → 80 (+167%)
- **Balanced representation** - All backyard species now have 80-120 samples for consistent performance
- **Hybrid training approach** - Your local expertise + professional reference images = superior accuracy

#### ⚡ **Optimized Training Pipeline**
- **4x faster training** on Apple Silicon - Advanced optimizations reduce training time dramatically
- **Mixed precision training** - Leverages M4 Pro neural engine for maximum speed
- **Enhanced data augmentation** - Better generalization through aggressive image transformations
- **Learning rate scheduling** - Smooth convergence with adaptive learning rates
- **Early stopping** - Prevents overfitting with intelligent patience mechanisms

#### 🔄 **Automated Learning System**
- **Daily auto-retraining** runs at 11:00 PM when 15+ new identifications collected
- **Enhanced pipeline integration** - Uses optimized training automatically
- **Automatic model reload** - Service picks up new model without restart
- **Cross-location learning** - Data from multiple cameras improves accuracy
- **Quality control** - Only human-verified data used for continuous improvement
- **Training logs** track model improvements over time with detailed metrics

#### 📊 **Performance Comparison**
| Platform | Training Time | GPU Support | Service Management |
|----------|---------------|-------------|-------------------|
| **Mac M4 Pro** | **15 minutes** | ✅ Metal | ✅ Native launchd |
| WSL2/Linux | 2+ hours | ⚠️ Limited | 🔧 Manual setup |
| Windows | 2+ hours | ⚠️ Complex | 🔧 Manual setup |

## 🏗️ Architecture

### Core Components

#### 🔧 **Two-Service Architecture**
- **`run.py`** - 📹 Camera monitoring service (detects birds, sends alerts)
- **`discord_bot.py`** - 💬 Discord response service (processes human feedback)

#### 🧠 **AI Training System**
- **`bird_trainer_enhanced.py`** - 🚀 **Apple Silicon optimized training with NABirds integration**
- **`nabirds_extractor.py`** - 🎯 **NABirds professional dataset extraction and curation**
- **`custom_bird_classifier.py`** - Enhanced classifier with automatic model selection
- **`auto_retrain.py`** - Automated retraining trigger system

#### 📱 **Service Management (macOS)**
- **`service-install-all.sh`** - Install both services as background daemons
- **`service-status-all.sh`** - Check status of both services
- **`service-start-all.sh`** / **`service-stop-all.sh`** - Control services
- **`service-logs-all.sh`** - View logs from both services
- **`service-uninstall-all.sh`** - Remove services completely

#### 🛠 **Setup and Compatibility**
- **`setup-mac-py312.sh`** - One-command Mac setup with Apple Silicon optimization
- **`check_compatibility.py`** - System compatibility verification
- **`requirements-mac.txt`** - Mac-optimized dependencies
- **`README-SERVICE.md`** - Complete service management guide

#### 🔧 **Core Infrastructure**
- **`camera_manager.py`** - Multi-camera management and location-aware processing
- **`species_mapping.py`** - Species classification and location mapping
- **`photo_organizer.py`** - Location-aware photo organization
- **`training_improvements_summary.py`** - Training performance tracking

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
Multi-Location Corrections → Training Check → Enhanced NABirds Training → Auto Reload
          ↓                      ↓                    ↓                      ↓
   (15+ cross-location) → Triggers Training → Professional + Local Data → Superior AI
                                              ↓
                                  3-5x Faster Pipeline + Mixed Precision
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
├── 🚀 SERVICES (Two-process architecture)
│   ├── run.py                         # 📹 Camera monitoring service
│   └── discord_bot.py                 # 💬 Discord response service
│
├── 🛠 MAC SETUP (Apple Silicon optimized)
│   ├── setup-mac-py312.sh            # One-command Mac setup
│   ├── check_compatibility.py        # System verification
│   ├── requirements-mac.txt          # Mac-optimized dependencies
│   └── fix_distutils.py             # Python 3.12 compatibility
│
├── 📱 SERVICE MANAGEMENT (macOS launchd)
│   ├── service-install-all.sh        # Install both services
│   ├── service-status-all.sh         # Check service status
│   ├── service-start-all.sh          # Start services
│   ├── service-stop-all.sh           # Stop services
│   ├── service-logs-all.sh           # View service logs
│   ├── service-uninstall-all.sh      # Remove services
│   ├── com.fountainbuddy.service.plist     # Camera service config
│   ├── com.fountainbuddy.discordbot.plist  # Discord service config
│   └── README-SERVICE.md             # Service documentation
│
├── 🧠 AI TRAINING (Apple Silicon accelerated)
│   ├── bird_trainer_enhanced.py      # 🚀 M4 Pro optimized training
│   ├── nabirds_extractor.py          # NABirds dataset integration
│   ├── custom_bird_classifier.py     # Enhanced classifier
│   ├── auto_retrain.py               # Automated retraining
│   └── training_improvements_summary.py # Performance tracking
│
├── 🔧 CORE INFRASTRUCTURE
│   ├── camera_manager.py             # Multi-camera management
│   ├── species_mapping.py            # Species classification
│   ├── photo_organizer.py            # Photo organization
│   └── photo_cleanup_scheduler.py    # Cleanup automation
│
├── 📊 DATA & MODELS
│   ├── models/                       # Trained AI models
│   ├── training_data_unified/        # Training images (human + NABirds)
│   ├── nabirds_training_data/        # Professional reference images
│   ├── bird_images/                  # Captured bird photos
│   │   ├── fountain/                 # Fountain camera
│   │   ├── peanut/                   # Peanut feeder camera
│   │   └── archive/                  # Archived images
│   ├── logs/                         # Service logs
│   │   ├── fountain-buddy.log        # Camera service logs
│   │   ├── discord-bot.log           # Discord service logs
│   │   └── *-error.log              # Error logs
│   └── fountain_buddy.db             # SQLite database
│
├── 📚 DOCUMENTATION
│   ├── memory-bank/                  # Project evolution docs
│   │   ├── project-overview.md       # System overview
│   │   ├── mac-migration-success.md  # 🆕 Migration results
│   │   └── performance-improvements.md # 🆕 Benchmarks
│   ├── requirements.txt              # Legacy requirements
│   ├── .env.example                  # Configuration template
│   └── README.md                     # This file
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