# Multi-Camera Expansion Plan - Peanut Feeder Addition

## 🎯 Project Goal
Add a second Reolink camera pointing at a peanut feeder to monitor a different set of birds, with separate Discord channel for notifications.

## 📊 Species Analysis

### Current Fountain Birds (10 species)
- Northern Cardinal, American Robin, Common Grackle, Blue Jay, Mourning Dove
- House Sparrow, Gray Catbird, House Finch, Song Sparrow, European Starling

### New Peanut Feeder Birds (7 species)  
- Red-bellied Woodpecker, Black-capped Chickadee, Northern Flicker
- White-breasted Nuthatch, Tufted Titmouse, Carolina Wren, European Starling

### Overlap Analysis
- **Only overlap**: European Starling (appears at both locations)
- **Total unique species**: 16 species
- **Total classifier classes**: 17 (including existing Squirrel class)

## 🤖 AI Classifier Strategy: Unified Model (Recommended)

### Why Unified Classifier?
- **Single model** - easier maintenance, one training pipeline
- **Cross-location learning** - European Starling data from both locations improves accuracy
- **Better generalization** - more diverse training data (16 bird species + squirrel)
- **Simpler deployment** - no model routing logic needed

### Model Expansion
- **Current**: 13 classes, 994 training samples
- **Target**: 17 classes (add 6 peanut species, remove Red-winged Blackbird if needed)
- **Training**: Extend existing ResNet-50 fine-tuning with new species

## 🏗️ Architecture Changes

### 1. Environment Variables (.env)
```bash
# Camera 1 - Fountain (existing, renamed)
FOUNTAIN_CAMERA_IP=192.168.1.100
FOUNTAIN_USERNAME=username
FOUNTAIN_PASSWORD=password
FOUNTAIN_RTSP_PORT=554
FOUNTAIN_HTTP_PORT=80

# Camera 2 - Peanut Feeder (new)
PEANUT_CAMERA_IP=192.168.1.101
PEANUT_USERNAME=username  
PEANUT_PASSWORD=password
PEANUT_RTSP_PORT=554
PEANUT_HTTP_PORT=80

# Discord - Fountain Channel (existing)
DISCORD_WEBHOOK_FOUNTAIN=https://discord.com/api/webhooks/FOUNTAIN_WEBHOOK
DISCORD_CHANNEL_FOUNTAIN_ID=channel_id

# Discord - Peanut Channel (new)
DISCORD_WEBHOOK_PEANUT=https://discord.com/api/webhooks/PEANUT_WEBHOOK
DISCORD_CHANNEL_PEANUT_ID=channel_id
```

### 2. Database Schema Updates
```sql
-- Add location tracking
ALTER TABLE bird_visits ADD COLUMN location TEXT DEFAULT 'fountain';
ALTER TABLE bird_visits ADD COLUMN camera_id TEXT DEFAULT 'fountain';

-- Update existing records
UPDATE bird_visits SET location = 'fountain', camera_id = 'fountain';
```

### 3. File Structure Changes
```
bird_images/
├── fountain/              # Migrate from existing active/
│   ├── bird_American_Robin_2025-07-18_14-30-15.jpg
│   └── ...
└── peanut/               # New directory
    ├── bird_Red_bellied_Woodpecker_2025-07-18_15-30-15.jpg
    └── ...

training_data/
├── fountain/             # Location-specific training data
│   ├── American_Robin/
│   └── ...
└── peanut/              # New training data
    ├── Red_bellied_Woodpecker/
    └── ...
```

### 4. Core Code Architecture

**Camera Management Class:**
```python
class CameraManager:
    def __init__(self, camera_id, location, ip, username, password, webhook_url, channel_id):
        self.camera_id = camera_id
        self.location = location
        self.config = {...}
        self.common_birds = LOCATION_BIRDS[location]
    
    def get_detection_state(self):
        # Camera-specific API calls
    
    def capture_snapshot(self):
        # Camera-specific snapshot logic
```

**Multi-Camera Main Loop:**
```python
def main_loop():
    cameras = [
        CameraManager('fountain', 'fountain', fountain_config),
        CameraManager('peanut', 'peanut', peanut_config)
    ]
    
    while True:
        for camera in cameras:
            if camera.motion_detected():
                process_bird_detection(camera)
        time.sleep(1)
```

## 📱 Discord Integration Strategy

### Two-Channel Setup
- **#fountain-birds** - Existing channel for fountain camera  
- **#peanut-birds** - New channel for peanut feeder camera

### Location-Specific Species Lists
```python
FOUNTAIN_BIRDS = {
    1: "Northern Cardinal", 2: "American Robin", 3: "Common Grackle",
    4: "Blue Jay", 5: "Mourning Dove", 6: "House Sparrow",
    7: "Gray Catbird", 8: "House Finch", 9: "Song Sparrow", 
    10: "European Starling"
}

PEANUT_BIRDS = {
    1: "Red-bellied Woodpecker", 2: "Black-capped Chickadee",
    3: "Northern Flicker", 4: "White-breasted Nuthatch", 
    5: "Tufted Titmouse", 6: "Carolina Wren", 7: "European Starling"
}
```

### Enhanced Discord Messages
```
🥜 **New bird at peanut feeder!** YOLO confidence: 0.85
🤖 AI thinks: Black-capped Chickadee (0.73)

What species is this? Reply with number:
1. Red-bellied Woodpecker
2. Black-capped Chickadee
3. Northern Flicker
4. White-breasted Nuthatch
5. Tufted Titmouse  
6. Carolina Wren
7. European Starling

📁 File: bird_Black_capped_Chickadee_2025-07-18_14-30-15.jpg
📍 Location: Peanut Feeder
```

### Discord Bot Updates
- **Multi-channel monitoring** - bot listens to both channels
- **Location-aware responses** - different species lists per channel
- **Enhanced file naming** - include location in filename pattern
- **Cross-location corrections** - handle species corrections per location

## 🗃️ Database Design

### Updated Schema
```sql
CREATE TABLE bird_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    bird_type TEXT NOT NULL,
    species TEXT,
    confidence REAL,
    image_path TEXT,
    location TEXT DEFAULT 'fountain',      -- NEW: fountain/peanut
    camera_id TEXT DEFAULT 'fountain'      -- NEW: camera identifier
);
```

### Migration Strategy
```sql
-- Step 1: Add columns with defaults
ALTER TABLE bird_visits ADD COLUMN location TEXT DEFAULT 'fountain';
ALTER TABLE bird_visits ADD COLUMN camera_id TEXT DEFAULT 'fountain';

-- Step 2: Update existing records (all fountain data)
UPDATE bird_visits SET location = 'fountain', camera_id = 'fountain';

-- Step 3: Update image paths for new structure
-- (Handle during file migration script)
```

## 🚀 Implementation Timeline

### Phase 1: Foundation (Week 1)
- [ ] Database schema updates and migration
- [ ] File structure reorganization (move active/ to fountain/)
- [ ] Environment variable updates (.env changes)
- [ ] Camera management class implementation

### Phase 2: Core Multi-Camera Logic (Week 2)
- [ ] Multi-camera detection loop
- [ ] Location-aware image saving and database recording
- [ ] Discord integration updates (dual webhook support)
- [ ] Species list configuration per location

### Phase 3: AI Model Updates (Week 3)
- [ ] Extend classifier from 13 to 17 classes
- [ ] Collect initial peanut feeder training data
- [ ] Retrain unified model with combined dataset
- [ ] Update training pipeline for multi-location data

### Phase 4: Testing & Deployment (Week 4)
- [ ] End-to-end testing with both cameras
- [ ] Performance optimization and error handling
- [ ] Documentation updates (README, memory-bank)
- [ ] Production deployment and monitoring

## 🔧 Configuration Management

### Backwards Compatibility
- Existing single-camera config still works
- Gradual migration path for environment variables
- Database migration handles existing data gracefully

### New Configuration Required
1. **Second camera network setup** (IP, credentials)
2. **Second Discord webhook and channel creation**
3. **Species list configuration per location**
4. **File structure migration script**

## 📈 Benefits

### Enhanced Monitoring
- **Doubled bird species coverage** (10 → 16+ species)
- **Location-specific insights** - different birds prefer different food sources
- **Better training data diversity** - more varied poses, lighting, backgrounds

### Improved AI Performance
- **Cross-location learning** - European Starling data from both locations
- **More robust classification** - 17 classes with diverse training data
- **Better generalization** - model learns birds in different contexts

### Operational Advantages
- **Separate Discord channels** - cleaner notifications per location
- **Location-aware analytics** - daily reports can show per-location stats
- **Scalable architecture** - easy to add 3rd, 4th cameras in future

## 🎯 Success Metrics

### Technical
- [ ] Both cameras operational with <30s detection latency
- [ ] >80% AI classification accuracy across all 17 species  
- [ ] Zero data loss during migration
- [ ] Discord notifications working in both channels

### Operational  
- [ ] Daily reports include both locations
- [ ] Auto-retraining works with combined dataset
- [ ] Human correction workflow functions for both cameras
- [ ] File organization maintains consistency across locations