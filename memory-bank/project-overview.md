# Fountain Buddy - Project Overview

## 📋 Quick Summary
**Fountain Buddy** is an AI-powered bird identification system that combines computer vision with human expertise to create an accurate backyard bird monitoring system. It watches a fountain/water feature, detects birds, identifies species using AI, then sends Discord notifications for human verification.

## 🏗️ Architecture & Components

### Core Files
- **`run.py`** - Main application with camera monitoring, YOLO detection, and species classification
- **`discord_bot.py`** - Bot that processes human identification responses via Discord
- **`bird_trainer.py`** - AI model training system using transfer learning (ResNet-50)
- **`auto_retrain.py`** - Automated retraining trigger when 15+ corrections collected
- **`custom_bird_classifier.py`** - Custom bird species classifier wrapper
- **`photo_cleanup_scheduler.py`** - Automated photo organization and cleanup
- **`photo_organizer.py`** - Core photo organization logic

### Data Structure
- **`bird_images/active/`** - Current bird photos (renamed with species after identification)
- **`training_data/`** - Organized photos for AI model training
- **`models/`** - Trained AI models (custom classifier)
- **`fountain_buddy.db`** - SQLite database with bird visit records

## 🔄 Workflow

### 1. Detection Phase
1. Camera monitors for motion/AI triggers (Reolink integration)
2. YOLO detects and crops birds from images
3. Custom classifier predicts species
4. Image saved with timestamp

### 2. Human Verification
1. Discord notification sent with image + AI prediction + numbered species options
2. Human replies with number (1-10) or species name
3. Database updated with verified species
4. Image renamed to include correct species

### 3. Continuous Learning
1. Verified identifications become training data
2. Auto-retraining triggers nightly at 11 PM when 15+ new samples collected
3. New model automatically loaded without restart
4. AI accuracy improves over time

## 🛠️ Technology Stack

### Hardware/External
- **Reolink camera** with AI detection capability
- **Discord** for human-in-the-loop verification
- **Email** for daily summaries

### AI/ML
- **YOLOv8** for bird detection and cropping
- **Custom ResNet-50** fine-tuned for local bird species
- **Transfer learning** pipeline for continuous improvement

### Backend
- **Python 3.8+** with virtual environment
- **SQLite** database for visit records
- **OpenCV** for image processing
- **TensorFlow/Keras** for neural networks
- **APScheduler** for automated tasks

## 📊 Key Features

### Smart Detection
- Motion/AI triggered capture (efficient monitoring)
- YOLO bird detection (never miss a visitor)
- Species classification (AI + human verification)

### Human-AI Collaboration
- Discord integration with numbered quick responses
- Real-time database updates and file renaming
- Confidence tracking (AI vs human accuracy)

### Self-Training System
- Automated model retraining (nightly at 11 PM)
- Quality control (human-verified data only)
- Continuous accuracy improvement

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