# Bird Classifier Improvement System

This system improves the ResNet-50 bird identification accuracy by using human corrections to train a custom model focused on your specific backyard bird species.

## 🎯 Overview

The original system used a generic ImageNet ResNet-50 that could identify 1000+ classes but struggled with bird species accuracy (only Robins worked well). This new system creates a focused classifier trained on your human-verified bird data.

## 📁 Files Added

- **`bird_trainer.py`** - Main training pipeline that fine-tunes ResNet-50
- **`custom_bird_classifier.py`** - Production integration wrapper
- **`auto_retrain.py`** - Automated retraining system
- **`BIRD_CLASSIFIER_IMPROVEMENT.md`** - This documentation

## 🚀 Initial Setup & Training

### Step 1: Train Your First Custom Model
```bash
python3 bird_trainer.py
```

This will:
- Load your human-verified bird data from the database
- Organize images by species for training
- Fine-tune ResNet-50 on your specific bird species
- Save the trained model to `models/fountain_buddy_bird_classifier.h5`
- Create metadata file with species information

### Step 2: Integrate with Main Application

Add to the top of `run.py`:
```python
from custom_bird_classifier import CustomBirdClassifier
```

In your main initialization section:
```python
# Initialize custom bird classifier
custom_classifier = CustomBirdClassifier()
custom_classifier.load_model()
```

Replace your existing `classify_bird_species()` function with:
```python
def classify_bird_species(image_crop):
    """Classify bird species using custom model with fallback"""
    try:
        if custom_classifier.is_loaded:
            result = custom_classifier.predict(image_crop)
            print(f"Custom classifier: {result['species']} ({result['confidence']:.2f})")
            if result['confidence'] > 0.3:  # High confidence threshold
                return result['species'], result['confidence']
    except Exception as e:
        print(f"Custom classifier error: {e}")
    
    # Fall back to original ImageNet classifier
    return original_classify_bird_species(image_crop)
```

## 🔄 Automated Retraining

### Manual Retraining Check
```bash
# Check if retraining is needed
python3 auto_retrain.py --check-only

# Force retraining
python3 auto_retrain.py --force
```

### Automatic Retraining Integration

Add to your `run.py` main loop or daily summary function:
```python
from auto_retrain import AutoRetrainer

def check_for_model_updates():
    """Check if model needs retraining"""
    retrainer = AutoRetrainer(min_new_samples=15)
    if retrainer.check_and_retrain():
        # Reload the custom classifier with new model
        custom_classifier.load_model()
```

## 📊 Expected Results

### Before (Generic ImageNet)
- American Robin: ~100% accuracy
- Other species: Poor accuracy (high false positives)

### After (Custom Fine-tuned Model)
- All 6 species: Significantly improved accuracy
- Focused on your actual backyard birds
- Reduced false positives from irrelevant ImageNet classes

## 🔧 Production Deployment Steps

1. **Stop running applications**
   ```bash
   # Stop fountain monitoring
   pkill -f run.py
   
   # Stop Discord bot
   pkill -f discord_bot.py
   ```

2. **Deploy new files**
   ```bash
   git add bird_trainer.py custom_bird_classifier.py auto_retrain.py BIRD_CLASSIFIER_IMPROVEMENT.md
   git commit -m "Add custom bird classifier training system"
   git push
   ```

3. **On production server**
   ```bash
   git pull
   python3 bird_trainer.py  # Train initial model
   ```

4. **Update run.py** with integration code (see Step 2 above)

5. **Restart applications**
   ```bash
   # Start fountain monitoring
   python3 run.py &
   
   # Start Discord bot
   python3 discord_bot.py &
   ```

## 🎯 Training Data Requirements

### Minimum Requirements
- **10+ human-verified samples** for basic training
- **15+ new samples** to trigger automatic retraining

### Current Data (as of implementation)
- **89 human-verified species** total
- **6 distinct species** with good distribution:
  - American Robin: 19 samples
  - Northern Cardinal: 17 samples
  - Starling: 16 samples
  - House Sparrow: 14 samples
  - Mourning Dove: 12 samples
  - Gray Catbird: 8 samples

## 🔍 Troubleshooting

### Training Fails
- Check that `bird_images/` directory exists and contains images
- Verify database has human-verified entries (confidence = 1.0)
- Check that images from July 3+ are available

### Model Not Loading
- Ensure `models/fountain_buddy_bird_classifier.h5` exists
- Check `models/model_metadata.json` for class information
- Verify TensorFlow/Keras installation

### Poor Accuracy
- Need more training samples per species (aim for 15+ each)
- Consider adjusting confidence threshold in integration code
- Check that training images match the species labels

## 📈 Monitoring & Maintenance

### Weekly Checks
```bash
# Check for new corrections
python3 auto_retrain.py --check-only

# View training logs
cat auto_retrain.log
```

### Monthly Review
- Review species distribution in database
- Check model performance logs
- Consider manual retraining if needed

## 🎉 Expected Impact

This system should dramatically improve your bird identification accuracy beyond just Robins. The custom model will be specifically tuned to your backyard birds and will continuously improve as you provide more human corrections through Discord.

The automated retraining ensures the model stays current with new bird species and seasonal variations in your area.