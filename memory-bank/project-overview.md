# Fountain Buddy - Project Overview

## 📋 Quick Summary
**Fountain Buddy** is an AI-powered bird identification system optimized for Apple Silicon that combines computer vision with human expertise to create an accurate backyard bird monitoring system. It watches multiple camera locations (fountain, feeders, etc.), detects birds, identifies species using AI, then sends Discord notifications for human verification.

## 🚀 Platform Status (July 2025)
**Primary Platform**: **Mac M4 Pro** (Apple Silicon)  
**Performance**: 4x faster training (15 minutes vs 2+ hours)  
**Reliability**: Native macOS services with auto-start/restart  
**Migration**: Successfully migrated from WSL2 to Mac with dramatic improvements

## 🏗️ Architecture & Components

### 🔧 Two-Service Architecture (Production)
- **`run.py`** - 📹 Camera monitoring service (bird detection, AI classification, Discord alerts)
- **`discord_bot.py`** - 💬 Discord response service (human feedback processing, database updates)

### 🧠 Custom CNN Training System (Apple Silicon Optimized) 
- **`train_clean_optimized_cnn.py`** - 🎯 **Working custom CNN trainer (64.6% accuracy breakthrough)**
- **`bird_trainer_enhanced_cnn.py`** - 🚀 **Production trainer with Discord corrections integration**
- **`nabirds_clean_extractor.py`** - 🎯 **Professional dataset extraction (1,596 balanced images)**
- **`auto_retrain.py`** - Automated retraining trigger (uses custom CNN approach)
- **`custom_bird_classifier.py`** - Enhanced classifier with automatic clean model selection

### 📱 Mac Service Management (macOS launchd)
- **`service-install-all.sh`** - Install both services as background daemons
- **`service-status-all.sh`** - Check system status (both services)
- **`service-start-all.sh`** / **`service-stop-all.sh`** - Control services
- **`service-logs-all.sh`** - View logs from both services
- **`README-SERVICE.md`** - Complete service management documentation

### 🛠 Mac Setup & Compatibility
- **`setup-mac-py312.sh`** - One-command Mac setup with Apple Silicon optimization
- **`check_compatibility.py`** - System compatibility verification for Mac
- **`requirements-mac.txt`** - Mac-optimized dependencies with TensorFlow Metal
- **`fix_distutils.py`** - Python 3.12 compatibility layer

### 🔧 Core Infrastructure
- **`photo_cleanup_scheduler.py`** - Automated photo organization and cleanup
- **`photo_organizer.py`** - Core photo organization logic
- **`camera_manager.py`** - Multi-camera management
- **`species_mapping.py`** - Species classification and location mapping

### Data Structure
- **`bird_images/`** - Captured bird photos organized by camera location
  - **`fountain/`** - Fountain camera captures
  - **`peanut/`** - Peanut feeder camera captures
  - **`archive/`** - Archived images
- **`nabirds_clean_training/`** - 🎯 **Clean NABirds foundation (1,596 balanced images, 96-100 per species)**
- **`training_data_enhanced_cnn/`** - 🚀 **Enhanced training data (clean foundation + Discord corrections)**
- **`models/`** - Trained AI models (M4 Pro enhanced models prioritized)
- **`logs/`** - Service logs (camera, Discord bot, errors)
- **`fountain_buddy.db`** - SQLite database with bird visit records

### Mac Service Configuration
- **`com.fountainbuddy.service.plist`** - Camera monitoring service config
- **`com.fountainbuddy.discordbot.plist`** - Discord bot service config
- **`~/Library/LaunchAgents/`** - macOS service installation directory

## 🔄 Workflow

### 🚀 Production Workflow (Mac Services)
Both services run automatically in background via macOS launchd:
- **Camera Service** continuously monitors cameras
- **Discord Bot Service** continuously listens for responses

### 1. Detection Phase
1. **Camera Service** (`run.py`) monitors for motion/AI triggers (Reolink integration)
2. YOLO detects and crops birds from images
3. Custom classifier predicts species
4. Image saved with timestamp

### 2. Human Verification
1. **Camera Service** sends Discord notification with image + AI prediction + species options
2. **Discord Bot Service** receives human reply (number 1-10 or species name)
3. **Discord Bot Service** updates database with verified species
4. Image renamed to include correct species and location

### 3. Continuous Learning (Apple Silicon Accelerated)
1. Verified identifications become training data
2. **Auto-retraining** triggers nightly at 11 PM when 15+ new samples collected
3. **M4 Pro training** completes in ~15 minutes (vs 2+ hours previously)
4. New model automatically loaded without service restart
5. AI accuracy improves rapidly with fast iteration cycle

## 🛠️ Technology Stack

### 🚀 Primary Platform: Apple Silicon (Mac M4 Pro)
- **macOS 15.5+** with native launchd service management
- **Python 3.12** with TensorFlow Metal GPU acceleration
- **Unified memory architecture** for efficient AI training
- **Apple Neural Engine** utilization for optimized inference

### Hardware/External
- **Reolink cameras** with AI detection capability (multi-location support)
- **Discord** for human-in-the-loop verification
- **Email** for daily summaries

### AI/ML (Apple Silicon Optimized)
- **YOLOv8** for bird detection and cropping
- **Enhanced ResNet-50** with NABirds professional training data integration
- **TensorFlow Metal** - Native Apple Silicon GPU acceleration
- **Hybrid training approach** - Local expertise + professional reference images
- **Optimized training pipeline** - Mixed precision, enhanced augmentation, LR scheduling
- **4x faster training** on M4 Pro (15 minutes vs 2+ hours on other platforms)
- **Transfer learning** pipeline for continuous improvement

### Service Architecture (macOS)
- **Two-service design** - Camera monitoring + Discord bot services
- **macOS launchd** - Native service management with auto-start/restart
- **Background operation** - No terminal windows required
- **Comprehensive logging** - Separate logs for each service

### Backend
- **Python 3.12** with virtual environment (Mac optimized)
- **SQLite** database for visit records and training metadata
- **TensorFlow 2.16+** with Metal backend for GPU acceleration
- **OpenCV** for image processing and computer vision
- **scikit-learn** for data preprocessing and metrics
- **APScheduler** for automated tasks (retraining, cleanup)
- **Discord.py** for bot integration
- **Ultralytics** for YOLO object detection

## 📊 Key Features

### Smart Detection
- Motion/AI triggered capture (efficient monitoring)
- YOLO bird detection (never miss a visitor)
- Species classification (AI + human verification)

### Human-AI Collaboration
- Discord integration with numbered quick responses
- Real-time database updates and file renaming
- Confidence tracking (AI vs human accuracy)

### Enhanced Self-Training System
- **NABirds-boosted training** - 265+ professional images for balanced datasets
- **Dramatic accuracy improvements** - Blue Jay: 8→80 samples (+900%), all species balanced
- **Optimized automated retraining** (nightly at 11 PM with enhanced pipeline)
- **3-5x faster training** - Minutes instead of hours
- **Hybrid quality control** - Human-verified data + curated professional images
- **Continuous accuracy improvement** with superior training data

### Data Management
- Organized file structure with species names
- Daily email summaries with accurate counts
- Long-term visit tracking and analysis

## 🔧 Configuration

### Environment Variables (`.env`)
- Camera connection (IP, credentials, ports)
- Discord integration (webhook, bot token, channel)
- Email settings (Gmail recommended)
- YOLO model configuration (confidence thresholds, cooldown)

### Database Schema
```sql
bird_visits (
    id, timestamp, bird_type, species, confidence, image_path
)
```

## 🎯 Current State & Recent Changes

### 🚀 **Major Enhancement: NABirds Integration (July 2025)**
- **Revolutionary training boost** - Integrated NABirds professional dataset
- **265+ additional training images** extracted and balanced across species
- **Massive accuracy improvements** - Blue Jay samples: 8 → 80 (+900% improvement)
- **All species balanced** - Every backyard species now has 80-120 training samples
- **Enhanced training pipeline** - 3-5x faster with mixed precision and optimizations
- **Automatic integration** - Enhanced system seamlessly integrated into existing workflow

### Previous Improvements
- Fixed bird classifier to prevent ImageNet fallback contamination
- Replaced Red-winged Blackbird with European Starling in species list
- Added auto-checkmark to original detection messages
- Improved automation to use virtual environment for training
- Active photo cleanup and organization system

## 📈 Daily Operations
- **11:00 PM**: Auto-retraining check + daily email summary
- **Continuous**: Bird detection, Discord notifications, human verification
- **Background**: Photo organization and cleanup scheduling

## 🚀 Deployment & Services
- **`fountain-buddy`** - systemd service running main detection loop (run.py)
- **`discordbot`** - systemd service running Discord monitoring (discord_bot.py)
- **Restart both services** after configuration changes:
  ```bash
  sudo systemctl restart fountain-buddy
  sudo systemctl restart discordbot
  ```

## 🐦 Common Bird Species (Numbered List)
1. Northern Cardinal
2. American Robin
3. Common Grackle
4. Blue Jay
5. Mourning Dove
6. House Sparrow
7. American Goldfinch
8. European Starling
9. House Finch
10. Gray Catbird