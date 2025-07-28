#!/usr/bin/env python3
"""
Enhanced CNN Bird Trainer
Builds on the clean NABirds foundation with human Discord corrections
Uses proven custom CNN architecture (not transfer learning)
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
import sqlite3
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import cv2
import shutil
from datetime import datetime
import json
from pathlib import Path
import glob
from collections import Counter
import random

class EnhancedBirdTrainerCNN:
    def __init__(self, db_path='fountain_buddy.db', images_dir='bird_images', 
                 nabirds_clean_dir='nabirds_clean_training', unified_dir='training_data_enhanced_cnn'):
        self.db_path = db_path
        self.images_dir = images_dir
        self.nabirds_clean_dir = nabirds_clean_dir
        self.unified_dir = unified_dir
        self.model = None
        self.class_names = None
        
        # Training parameters
        self.img_size = (224, 224)
        self.batch_size = 16
        self.epochs = 100
        self.learning_rate = 0.001
        
        # Create directories
        self.model_dir = 'models'
        os.makedirs(self.unified_dir, exist_ok=True)
        os.makedirs(self.model_dir, exist_ok=True)
        
    def load_human_verified_data(self):
        """Load human-verified corrections from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT species, image_path FROM bird_visits 
            WHERE species IS NOT NULL 
            AND confidence = 1.0 
            AND species NOT IN ('Unknown; Not A Bird', 'Not A Bird', 'skip')
            AND image_path IS NOT NULL
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        return results

    def create_enhanced_dataset(self):
        """Create unified dataset: clean NABirds foundation + human corrections"""
        print("🔄 Creating enhanced dataset with human corrections...")
        
        # Clear existing unified data
        if os.path.exists(self.unified_dir):
            shutil.rmtree(self.unified_dir)
        os.makedirs(self.unified_dir, exist_ok=True)
        
        # Balancing parameters
        MAX_SAMPLES_PER_SPECIES = 150
        MIN_SAMPLES_PER_SPECIES = 20
        
        # Step 1: Start with clean NABirds foundation
        print("📚 Starting with clean NABirds foundation...")
        clean_stats = Counter()
        
        for species_dir in Path(self.nabirds_clean_dir).iterdir():
            if species_dir.is_dir():
                species_name = species_dir.name
                dest_species_dir = Path(self.unified_dir) / species_name
                dest_species_dir.mkdir(exist_ok=True)
                
                # Copy all NABirds images (already balanced at ~100 each)
                for img_file in species_dir.glob("*.jpg"):
                    dest_path = dest_species_dir / f"nabirds_{img_file.name}"
                    shutil.copy2(img_file, dest_path)
                    clean_stats[species_name] += 1
        
        print(f"✅ Copied {sum(clean_stats.values())} clean NABirds images")
        
        # Step 2: Add human corrections
        print("👥 Adding human corrections...")
        human_data = self.load_human_verified_data()
        human_stats = Counter()
        
        for species, image_path in human_data:
            if not species or not image_path:
                continue
                
            # Clean species name
            species_clean = species.replace(' - ', '_').replace(' ', '_').replace('-', '_')
            
            # Check if we have this species in our clean dataset
            dest_species_dir = Path(self.unified_dir) / species_clean
            if not dest_species_dir.exists():
                print(f"⚠️ Skipping {species} - not in clean foundation")
                continue
            
            # Check current count
            current_count = len(list(dest_species_dir.glob("*.jpg")))
            if current_count >= MAX_SAMPLES_PER_SPECIES:
                continue  # Skip if already at cap
            
            # Copy human correction
            source_path = Path(image_path)
            if source_path.exists():
                dest_filename = f"human_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{source_path.name}"
                dest_path = dest_species_dir / dest_filename
                try:
                    shutil.copy2(source_path, dest_path)
                    human_stats[species_clean] += 1
                except Exception as e:
                    print(f"⚠️ Failed to copy {source_path}: {e}")
        
        print(f"✅ Added {sum(human_stats.values())} human corrections")
        
        # Step 3: Generate final stats
        final_stats = {}
        for species_dir in Path(self.unified_dir).iterdir():
            if species_dir.is_dir():
                count = len(list(species_dir.glob("*.jpg")))
                if count >= MIN_SAMPLES_PER_SPECIES:
                    final_stats[species_dir.name] = count
                else:
                    print(f"⚠️ Removing {species_dir.name} - only {count} samples")
                    shutil.rmtree(species_dir)
        
        # Report
        print(f"\n📊 Enhanced Dataset Summary:")
        print(f"Species: {len(final_stats)}")
        print(f"Total images: {sum(final_stats.values())}")
        
        for species, count in sorted(final_stats.items()):
            human_added = human_stats.get(species, 0)
            nabirds_base = clean_stats.get(species, 0)
            status = "CAPPED" if count >= MAX_SAMPLES_PER_SPECIES else "BALANCED"
            print(f"  {species.replace('_', ' '):25}: {count:3d} ({nabirds_base} NABirds + {human_added} human) [{status}]")
        
        return final_stats

    def create_enhanced_cnn(self, num_classes):
        """Create the same proven custom CNN architecture"""
        print(f"🏗️ Creating enhanced CNN for {num_classes} classes...")
        
        model = Sequential([
            # Block 1
            Conv2D(32, (3, 3), activation='relu', input_shape=(*self.img_size, 3)),
            BatchNormalization(),
            Conv2D(32, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Block 2
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Block 3
            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Block 4
            Conv2D(256, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(256, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Block 5
            Conv2D(512, (3, 3), activation='relu'),
            BatchNormalization(),
            GlobalAveragePooling2D(),
            
            # Classification head
            Dropout(0.5),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=self.learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

    def train_enhanced_model(self):
        """Train enhanced model with human corrections"""
        print("🚀 Enhanced CNN Training with Human Corrections")
        print("=" * 60)
        
        # Create enhanced dataset
        final_stats = self.create_enhanced_dataset()
        
        if not final_stats:
            print("❌ No valid species found!")
            return None
        
        # Setup data generators
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=30,
            width_shift_range=0.25,
            height_shift_range=0.25,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.15,
            brightness_range=[0.8, 1.2],
            validation_split=0.2
        )
        
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=0.2
        )
        
        train_generator = train_datagen.flow_from_directory(
            self.unified_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        val_generator = val_datagen.flow_from_directory(
            self.unified_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        self.class_names = list(train_generator.class_indices.keys())
        num_classes = len(self.class_names)
        
        print(f"✅ Training: {train_generator.samples}, Validation: {val_generator.samples}")
        
        # Create model
        self.model = self.create_enhanced_cnn(num_classes)
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy',
                patience=20,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.3,
                patience=8,
                min_lr=1e-8,
                verbose=1
            )
        ]
        
        # Train
        print("🚀 Starting enhanced training...")
        history = self.model.fit(
            train_generator,
            epochs=self.epochs,
            validation_data=val_generator,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate
        val_loss, val_accuracy = self.model.evaluate(val_generator, verbose=0)
        
        # Save model
        model_path = Path(self.model_dir) / "enhanced_nabirds_cnn.keras"
        self.model.save(model_path)
        
        # Save metadata
        metadata = {
            "model_path": str(model_path),
            "class_names": [name.replace('_', ' ') for name in self.class_names],
            "num_classes": num_classes,
            "image_size": list(self.img_size),
            "training_date": datetime.now().isoformat(),
            "data_source": "clean_nabirds_plus_human_corrections",
            "total_training_samples": train_generator.samples,
            "total_validation_samples": val_generator.samples,
            "final_accuracy": float(history.history['accuracy'][-1]),
            "final_val_accuracy": float(val_accuracy),
            "best_val_accuracy": float(max(history.history['val_accuracy'])),
            "epochs_completed": len(history.history['accuracy']),
            "species_distribution": final_stats,
            "model_architecture": "Enhanced Custom CNN (NABirds + Human)",
            "improvements": [
                "clean_nabirds_foundation_64_6_percent",
                "human_discord_corrections_added",
                "custom_cnn_not_transfer_learning",
                "caps_maintained_150_per_species"
            ]
        }
        
        metadata_path = Path(self.model_dir) / "enhanced_nabirds_cnn_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        best_acc = max(history.history['val_accuracy'])
        print(f"\n🎉 Enhanced training complete!")
        print(f"📈 Best validation accuracy: {best_acc:.3f}")
        print(f"💾 Model: {model_path}")
        print(f"💾 Metadata: {metadata_path}")
        
        return metadata

def main():
    trainer = EnhancedBirdTrainerCNN()
    metadata = trainer.train_enhanced_model()
    
    if metadata:
        print("\n✅ Enhanced CNN training successful!")
        print("🔄 Update custom_bird_classifier.py to use enhanced_nabirds_cnn.keras")

if __name__ == "__main__":
    main()