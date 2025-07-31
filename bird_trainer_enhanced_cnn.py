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
import re

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
    
    def resolve_image_path(self, expected_path, species_name):
        """
        Robust file resolution that handles naming variations.
        Tries multiple strategies to find the actual image file.
        """
        expected_path = Path(expected_path)
        
        # Strategy 1: Try the exact path
        if expected_path.exists():
            return expected_path
        
        # Strategy 2: Try in bird_images/active directory
        active_path = Path(self.images_dir) / "active" / expected_path.name
        if active_path.exists():
            return active_path
        
        # Strategy 3: Extract key components from filename for fuzzy matching
        # Expected format might be: human_20250729_230022_bird_Tufted_Titmouse_2025-07-25_09-17-12.jpg
        # Actual format might be: human_bird_Tufted_Titmouse_2025-07-25_09-17-12.jpg
        filename = expected_path.name
        
        # Extract date and time components using regex
        date_pattern = r'(\d{4}-\d{2}-\d{2})'
        time_pattern = r'(\d{2}-\d{2}-\d{2})'
        
        date_match = re.search(date_pattern, filename)
        time_match = re.search(time_pattern, filename)
        
        if date_match and time_match:
            date_str = date_match.group(1)
            time_str = time_match.group(1)
            species_clean = species_name.replace(' ', '_').replace('-', '_')
            
            # Strategy 4: Try simplified naming pattern
            # Look for: human_bird_Species_Date_Time.jpg
            simplified_name = f"human_bird_{species_clean}_{date_str}_{time_str}.jpg"
            
            # Check in active directory
            simplified_active_path = Path(self.images_dir) / "active" / simplified_name
            if simplified_active_path.exists():
                return simplified_active_path
            
            # Check in current directory
            simplified_current_path = Path(simplified_name)
            if simplified_current_path.exists():
                return simplified_current_path
        
        # Strategy 5: Try fuzzy matching in active directory based on species and timestamp
        if date_match and time_match:
            active_dir = Path(self.images_dir) / "active"
            if active_dir.exists():
                # Look for any file containing the species name, date, and time
                pattern = f"*{species_name.replace(' ', '*')}*{date_match.group(1)}*{time_match.group(1)}*"
                matching_files = list(active_dir.glob(pattern))
                if matching_files:
                    return matching_files[0]  # Return first match
        
        # Strategy 6: Search for any file with matching date/time in active directory
        if date_match and time_match:
            active_dir = Path(self.images_dir) / "active"
            if active_dir.exists():
                for img_file in active_dir.glob("*.jpg"):
                    if date_str in img_file.name and time_str in img_file.name:
                        return img_file
        
        # If all strategies fail, return the original path (will cause an error but with logging)
        print(f"⚠️ Could not resolve image path: {expected_path}")
        print(f"   Tried strategies: exact path, active directory, naming patterns, fuzzy matching")
        return expected_path
        
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
        
        # Create species name mapping: database name (spaces) -> NABirds name (underscores)
        species_mapping = {}
        
        for species_dir in Path(self.nabirds_clean_dir).iterdir():
            if species_dir.is_dir():
                nabirds_name = species_dir.name  # e.g., "Red-bellied_Woodpecker"
                db_name = nabirds_name.replace('_', ' ')  # e.g., "Red-bellied Woodpecker"
                species_mapping[db_name] = nabirds_name
                
                dest_species_dir = Path(self.unified_dir) / nabirds_name
                dest_species_dir.mkdir(exist_ok=True)
                
                # Copy all NABirds images (already balanced at ~100 each)
                img_files = list(species_dir.glob("*.jpg"))
                print(f"📁 Processing {nabirds_name} (DB: {db_name}): found {len(img_files)} NABirds images")
                
                for img_file in img_files:
                    try:
                        if img_file.exists():
                            # Don't add prefix if filename already starts with 'nabirds_'
                            if img_file.name.startswith('nabirds_'):
                                dest_path = dest_species_dir / img_file.name
                            else:
                                dest_path = dest_species_dir / f"nabirds_{img_file.name}"
                            shutil.copy2(img_file, dest_path)
                            clean_stats[nabirds_name] += 1
                        else:
                            print(f"⚠️ Source file does not exist: {img_file}")
                    except Exception as e:
                        print(f"⚠️ Failed to copy NABirds image {img_file}: {e}")
                
                if clean_stats[nabirds_name] == 0:
                    print(f"⚠️ No images copied for {nabirds_name} - removing directory")
                    if dest_species_dir.exists():
                        dest_species_dir.rmdir()
        
        print(f"✅ Copied {sum(clean_stats.values())} clean NABirds images")
        print(f"🗺️ Created species mapping for {len(species_mapping)} species")
        
        # Step 2: Add human corrections
        print("👥 Adding human corrections...")
        human_data = self.load_human_verified_data()
        human_stats = Counter()
        
        for species, image_path in human_data:
            if not species or not image_path:
                continue
                
            # Map database species name to NABirds directory name
            if species in species_mapping:
                nabirds_species_name = species_mapping[species]
                dest_species_dir = Path(self.unified_dir) / nabirds_species_name
            else:
                print(f"⚠️ Skipping {species} - not in clean foundation")
                continue
            
            # Smart sample management for capped species
            current_files = list(dest_species_dir.glob("*.jpg"))
            current_count = len(current_files)
            
            if current_count >= MAX_SAMPLES_PER_SPECIES:
                # Instead of skipping, replace the oldest NABirds image with this human correction
                nabirds_files = [f for f in current_files if f.name.startswith('nabirds_')]
                if nabirds_files:
                    # Find oldest NABirds file (by filename, since they maintain timestamp order)
                    oldest_nabirds = min(nabirds_files, key=lambda f: f.stat().st_mtime)
                    print(f"🔄 {nabirds_species_name} at cap ({current_count}/{MAX_SAMPLES_PER_SPECIES})")
                    print(f"   Replacing {oldest_nabirds.name} with human correction")
                    oldest_nabirds.unlink()  # Remove oldest NABirds image
                else:
                    print(f"⚠️ {nabirds_species_name} at cap with only human corrections - skipping")
                    continue
            
            # Copy human correction using robust file resolution
            try:
                resolved_path = self.resolve_image_path(image_path, species)
                if resolved_path.exists():
                    dest_filename = f"human_{resolved_path.name}"
                    dest_path = dest_species_dir / dest_filename
                    shutil.copy2(resolved_path, dest_path)
                    human_stats[nabirds_species_name] += 1
                else:
                    print(f"⚠️ Could not find image: {image_path} (resolved to: {resolved_path})")
            except Exception as e:
                print(f"⚠️ Failed to copy {image_path}: {e}")
        
        print(f"✅ Added {sum(human_stats.values())} human corrections (includes replacements for capped species)")
        
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
            
            # Count actual human vs nabirds files in final dataset
            species_dir = Path(self.unified_dir) / species
            actual_human = len(list(species_dir.glob("human_*.jpg")))
            actual_nabirds = len(list(species_dir.glob("nabirds_*.jpg")))
            human_ratio = actual_human / count if count > 0 else 0
            
            status = "CAPPED" if count >= MAX_SAMPLES_PER_SPECIES else "BALANCED"
            quality_indicator = "🏆" if human_ratio > 0.3 else "⭐" if human_ratio > 0.1 else ""
            
            print(f"  {species.replace('_', ' '):25}: {count:3d} ({actual_nabirds}N + {actual_human}H = {human_ratio:.1%} human) [{status}] {quality_indicator}")
        
        return final_stats

    def validate_training_data(self):
        """
        Validate that all training files exist and are accessible.
        Returns (is_valid, missing_files, total_files)
        """
        print("🔍 Validating training data files...")
        
        missing_files = []
        total_files = 0
        
        unified_path = Path(self.unified_dir)
        if not unified_path.exists():
            print(f"❌ Training directory does not exist: {unified_path}")
            return False, [], 0
        
        for species_dir in unified_path.iterdir():
            if species_dir.is_dir():
                for img_file in species_dir.glob("*.jpg"):
                    total_files += 1
                    if not img_file.exists():
                        missing_files.append(str(img_file))
                    
                    # Also check if file is readable
                    try:
                        with open(img_file, 'rb') as f:
                            f.read(1024)  # Try to read first 1KB
                    except Exception as e:
                        missing_files.append(f"{img_file} (unreadable: {e})")
        
        is_valid = len(missing_files) == 0
        
        if is_valid:
            print(f"✅ Training data validation passed: {total_files} files accessible")
        else:
            print(f"❌ Training data validation failed: {len(missing_files)}/{total_files} files missing or unreadable")
            for missing in missing_files[:10]:  # Show first 10 missing files
                print(f"   - {missing}")
            if len(missing_files) > 10:
                print(f"   ... and {len(missing_files) - 10} more")
        
        return is_valid, missing_files, total_files

    def evaluate_per_species_accuracy(self, val_generator):
        """Evaluate accuracy for each species individually"""
        print("🔍 Calculating per-species validation accuracy...")
        
        # Get predictions for validation set
        predictions = self.model.predict(val_generator, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = val_generator.classes
        
        # Map class indices to species names
        class_to_species = {v: k for k, v in val_generator.class_indices.items()}
        
        species_accuracy = {}
        species_counts = {}
        
        for true_idx, pred_idx in zip(true_classes, predicted_classes):
            true_species = class_to_species[true_idx]
            
            if true_species not in species_accuracy:
                species_accuracy[true_species] = {'correct': 0, 'total': 0}
            
            species_accuracy[true_species]['total'] += 1
            if true_idx == pred_idx:
                species_accuracy[true_species]['correct'] += 1
        
        # Calculate accuracy percentages
        species_results = {}
        for species, stats in species_accuracy.items():
            accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
            species_results[species] = {
                'accuracy': accuracy,
                'correct': stats['correct'],
                'total': stats['total']
            }
            print(f"  {species.replace('_', ' '):25}: {accuracy:.3f} ({stats['correct']}/{stats['total']})")
        
        return species_results
    
    def analyze_confidence_distribution(self, val_generator):
        """Analyze confidence distribution and calibration"""
        print("📈 Analyzing confidence distribution...")
        
        predictions = self.model.predict(val_generator, verbose=0)
        max_confidences = np.max(predictions, axis=1)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = val_generator.classes
        
        # Confidence bins
        confidence_bins = {
            'very_high': {'threshold': 0.9, 'correct': 0, 'total': 0},
            'high': {'threshold': 0.7, 'correct': 0, 'total': 0},
            'medium': {'threshold': 0.5, 'correct': 0, 'total': 0},
            'low': {'threshold': 0.0, 'correct': 0, 'total': 0}
        }
        
        for conf, pred, true in zip(max_confidences, predicted_classes, true_classes):
            # Determine confidence bin
            if conf >= 0.9:
                bin_name = 'very_high'
            elif conf >= 0.7:
                bin_name = 'high'
            elif conf >= 0.5:
                bin_name = 'medium'
            else:
                bin_name = 'low'
            
            confidence_bins[bin_name]['total'] += 1
            if pred == true:
                confidence_bins[bin_name]['correct'] += 1
        
        # Calculate calibration
        calibration_results = {}
        for bin_name, stats in confidence_bins.items():
            if stats['total'] > 0:
                accuracy = stats['correct'] / stats['total']
                calibration_results[bin_name] = {
                    'accuracy': accuracy,
                    'count': stats['total'],
                    'expected_min': confidence_bins[bin_name]['threshold']
                }
                print(f"  {bin_name.replace('_', ' ').title():12} confidence: {accuracy:.3f} accuracy ({stats['total']} samples)")
        
        overall_stats = {
            'mean_confidence': float(np.mean(max_confidences)),
            'median_confidence': float(np.median(max_confidences)),
            'std_confidence': float(np.std(max_confidences)),
            'calibration_by_bin': calibration_results
        }
        
        return overall_stats

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
        
        # Validate training data before proceeding
        is_valid, missing_files, total_files = self.validate_training_data()
        if not is_valid:
            print("❌ Training data validation failed! Cannot proceed with training.")
            print("💡 Tip: Check file paths in database and ensure images exist in expected locations.")
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
        
        # Comprehensive Evaluation
        print("📊 Running comprehensive model evaluation...")
        val_loss, val_accuracy = self.model.evaluate(val_generator, verbose=0)
        
        # Get per-species validation accuracy
        species_accuracy = self.evaluate_per_species_accuracy(val_generator)
        
        # Analyze confidence distribution
        confidence_stats = self.analyze_confidence_distribution(val_generator)
        
        # Save model
        model_path = Path(self.model_dir) / "enhanced_nabirds_cnn.keras"
        self.model.save(model_path)
        
        # Save comprehensive metadata
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
                "caps_maintained_150_per_species",
                "smart_sample_management_implemented"
            ],
            # New comprehensive evaluation metrics
            "evaluation_metrics": {
                "per_species_accuracy": species_accuracy,
                "confidence_analysis": confidence_stats,
                "training_history": {
                    "accuracy": [float(x) for x in history.history['accuracy']],
                    "val_accuracy": [float(x) for x in history.history['val_accuracy']],
                    "loss": [float(x) for x in history.history['loss']],
                    "val_loss": [float(x) for x in history.history['val_loss']]
                },
                "dataset_quality_metrics": {
                    "species_with_human_corrections": len([s for s, stats in final_stats.items() 
                                                         if Path(self.unified_dir).joinpath(s).glob("human_*.jpg")]),
                    "total_human_samples": sum(len(list(Path(self.unified_dir).joinpath(s).glob("human_*.jpg"))) 
                                             for s in final_stats.keys()),
                    "human_sample_ratio": sum(len(list(Path(self.unified_dir).joinpath(s).glob("human_*.jpg"))) 
                                            for s in final_stats.keys()) / sum(final_stats.values()) if sum(final_stats.values()) > 0 else 0
                }
            }
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