#!/usr/bin/env python3
"""
Custom Bird Classifier Integration
Replaces the generic ResNet-50 ImageNet classifier with a fine-tuned model
"""

# Python 3.12 compatibility fix
try:
    import distutils
except ImportError:
    import sys
    import importlib.util
    from unittest.mock import MagicMock
    
    distutils_spec = importlib.util.spec_from_loader("distutils", loader=None)
    distutils_module = importlib.util.module_from_spec(distutils_spec)
    distutils_module.version = MagicMock()
    distutils_module.spawn = MagicMock()
    distutils_module.util = MagicMock()
    
    sys.modules["distutils"] = distutils_module
    sys.modules["distutils.version"] = distutils_module.version
    sys.modules["distutils.spawn"] = distutils_module.spawn
    sys.modules["distutils.util"] = distutils_module.util

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import cv2

class CustomBirdClassifier:
    def __init__(self, model_path=None, metadata_path=None):
        """Initialize the custom bird classifier"""
        if model_path is None:
            # Use the enhanced CNN model by default
            self.model_path = 'models/enhanced_nabirds_cnn.keras'
            self.metadata_path = 'models/enhanced_nabirds_cnn_metadata.json'
            self.model_version = "enhanced_cnn"
        else:
            # Allow overriding for testing or other purposes
            self.model_path = model_path
            self.metadata_path = metadata_path
            self.model_version = "custom"
            
        self.model = None
        self.class_names = None
        self.is_loaded = False
        self.last_model_mtime = None  # Track model file modification time
        
    def load_model(self):
        """Load the trained bird classifier model"""
        if not os.path.exists(self.model_path):
            print(f"Custom model not found at {self.model_path}")
            return False
        
        if not os.path.exists(self.metadata_path):
            print(f"Model metadata not found at {self.metadata_path}")
            return False
        
        try:
            # Load model
            self.model = load_model(self.model_path)
            
            # Load metadata
            with open(self.metadata_path, 'r') as f:
                metadata = json.load(f)
            
            self.class_names = metadata['class_names']
            self.is_loaded = True
            
            # Track model file modification time for hot reloading
            self.last_model_mtime = os.path.getmtime(self.model_path)
            
            version_info = f" ({self.model_version})" if hasattr(self, 'model_version') else ""
            print(f"Loaded custom bird classifier{version_info} with {len(self.class_names)} species:")
            for i, species in enumerate(self.class_names):
                print(f"  {i}: {species}")
            
            return True
            
        except Exception as e:
            print(f"Error loading custom model: {e}")
            return False
    
    def preprocess_image(self, image):
        """Preprocess image for the custom model"""
        if isinstance(image, str):
            # Load image from path
            image = cv2.imread(image)
            if image is None:
                raise ValueError(f"Could not load image from {image}")
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize to 224x224 (ResNet-50 input size)
        image = cv2.resize(image, (224, 224))
        
        # Convert to array and normalize
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array = image_array / 255.0
        
        return image_array
    
    def predict(self, image):
        """Predict bird species using the custom model"""
        if not self.is_loaded:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Make prediction
        predictions = self.model.predict(processed_image, verbose=0)
        
        # Get top prediction
        top_idx = np.argmax(predictions[0])
        confidence = predictions[0][top_idx]
        species = self.class_names[top_idx]
        
        # Get top 3 predictions
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            (self.class_names[idx], float(predictions[0][idx]))
            for idx in top_3_idx
        ]
        
        return {
            'species': species,
            'confidence': float(confidence),
            'top_3': top_3_predictions
        }
    
    def check_for_model_updates(self):
        """Check if model file has been updated and reload if necessary"""
        if not os.path.exists(self.model_path):
            return False
            
        current_mtime = os.path.getmtime(self.model_path)
        
        # If model file is newer than our loaded version, reload
        if self.last_model_mtime is None or current_mtime > self.last_model_mtime:
            print(f"🔄 Model file updated, hot reloading {self.model_path}...")
            return self.load_model()
            
        return True
    
    def predict_with_fallback(self, image):
        """Predict bird species with fallback to Unknown Bird"""
        # Check for model updates before prediction
        if not self.check_for_model_updates():
            print("⚠️ Custom model not loaded or failed to reload, falling back to Unknown Bird")
            return "Unknown Bird", 0.0
        
        try:
            prediction = self.predict(image)
            species = prediction.get('species')
            confidence = float(prediction.get('confidence', 0.0))
            
            # Apply confidence threshold - lowered from 0.15 to 0.05
            if confidence < 0.05:
                print(f"🔄 Custom model prediction below threshold: {species} ({confidence:.3f}) → Unknown Bird")
                return "Unknown Bird", 0.0
            
            print(f"✅ Custom model prediction: {species} (confidence: {confidence:.3f})")
            return species, confidence
            
        except Exception as e:
            print(f"❌ Custom model prediction failed: {e} → Unknown Bird")
            return "Unknown Bird", 0.0


def integrate_with_main_app():
    """Integration instructions for the main application"""
    instructions = """
    Integration Instructions:
    =======================
    
    1. In run.py, import the custom classifier:
       from custom_bird_classifier import CustomBirdClassifier
    
    2. Initialize the classifier in the main function:
       custom_classifier = CustomBirdClassifier()
       custom_classifier.load_model()
    
    3. Replace the classify_bird_species function with:
       
       def classify_bird_species(image_crop):
           # Try custom classifier first
           if custom_classifier.is_loaded:
               result = custom_classifier.predict(image_crop)
               print(f"Custom classifier: {result['species']} ({result['confidence']:.2f})")
               return result['species'], result['confidence']
           
           # Fall back to original ImageNet classifier
           return original_classify_bird_species(image_crop)
    
    4. Create a retraining trigger function:
       
       def check_for_retraining():
           # Check if we have enough new human corrections
           conn = sqlite3.connect('fountain_buddy.db')
           cursor = conn.cursor()
           cursor.execute('''
               SELECT COUNT(*) FROM bird_visits 
               WHERE species IS NOT NULL AND confidence = 1.0 
               AND timestamp > (SELECT MAX(timestamp) FROM training_log)
           ''')
           new_corrections = cursor.fetchone()[0]
           conn.close()
           
           if new_corrections >= 20:  # Retrain every 20 new corrections
               print("Triggering model retraining...")
               os.system("./venv/bin/python bird_trainer_enhanced_cnn.py")
    
    5. Add retraining check to your daily summary or main loop
    """
    
    print(instructions)
    return instructions

if __name__ == "__main__":
    # Test the custom classifier
    classifier = CustomBirdClassifier()
    if classifier.load_model():
        print("Custom bird classifier loaded successfully!")
        # You can test with: result = classifier.predict("path/to/bird/image.jpg")
    else:
        print("Custom classifier not available. Run bird_trainer_enhanced_cnn.py first.")
        integrate_with_main_app()
