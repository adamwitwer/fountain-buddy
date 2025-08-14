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
from tensorflow.keras.utils import Sequence
import cv2
import shutil
from datetime import datetime
import json
from pathlib import Path
import glob
from collections import Counter
import random
import re
import pytz
from sklearn.utils import class_weight
import argparse

class WeightedDataGenerator(Sequence):
    def __init__(self, directory, image_paths, labels, class_indices, batch_size, target_size,
                 timestamps, augmentor, class_weights=None, shuffle=True, use_weights=True):
        self.directory = Path(directory)
        self.image_paths = image_paths
        self.labels = labels
        self.class_indices = class_indices
        self.batch_size = batch_size
        self.target_size = target_size
        self.timestamps = timestamps
        self.augmentor = augmentor
        self.class_weights = class_weights # Store class weights
        self.use_weights = use_weights
        self.shuffle = shuffle
        self.num_classes = len(class_indices)
        self.indices = np.arange(len(self.image_paths))
        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.image_paths) / self.batch_size))

    def __getitem__(self, index):
        batch_indices = self.indices[index * self.batch_size:(index + 1) * self.batch_size]
        batch_paths = [self.image_paths[i] for i in batch_indices]
        batch_labels = [self.labels[i] for i in batch_indices]
        
        X, y = self.__data_generation(batch_paths, batch_labels)
        
        if self.use_weights:
            # Pass batch_labels to get combined sample weights
            sample_weights = self.__get_sample_weights(batch_paths, batch_labels)
        else:
            # For validation, return uniform weights of 1. This is equivalent to no weighting.
            sample_weights = np.ones(len(batch_paths))
        
        return X, y, sample_weights

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __data_generation(self, batch_paths, batch_labels):
        X = np.empty((len(batch_paths), *self.target_size, 3))
        y = np.empty((len(batch_paths)), dtype=int)

        for i, path in enumerate(batch_paths):
            img = cv2.imread(str(path))
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, self.target_size)
                X[i,] = self.augmentor.random_transform(img) if self.augmentor else img
            else:
                print(f"Warning: Could not read image {path}. Replacing with zeros.")
                X[i,] = np.zeros((*self.target_size, 3))

            y[i] = batch_labels[i]

        # Rescale and convert to one-hot
        X = X / 255.0
        return X, tf.keras.utils.to_categorical(y, num_classes=self.num_classes)

    def __get_sample_weights(self, batch_paths, batch_labels):
        weights = np.ones(len(batch_paths))
        now = datetime.now()
        
        for i, path in enumerate(batch_paths):
            # 1. Calculate recency weight
            recency_weight = 1.0
            timestamp_str = self.timestamps.get(str(path))
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    if timestamp.tzinfo is None:
                        timestamp = timestamp.replace(tzinfo=pytz.UTC)
                    
                    now_aware = now.astimezone(pytz.UTC)

                    age = (now_aware - timestamp).total_seconds()
                    recency_weight = max(1.0, 2.0 - age / (30 * 24 * 3600))
                except (ValueError, TypeError) as e:
                    print(f"Warning: Could not parse timestamp '{timestamp_str}' for {path}. Using default weight. Error: {e}")
            
            # 2. Get class weight
            class_w = 1.0
            if self.class_weights:
                label = batch_labels[i]
                if label in self.class_weights:
                    class_w = self.class_weights[label]
            
            # 3. Combine weights
            weights[i] = recency_weight * class_w
            
        return weights

class EnhancedBirdTrainerCNN:
    def __init__(self, db_path='fountain_buddy.db', images_dir='bird_images', 
                 nabirds_clean_dir='nabirds_clean_training', unified_dir='training_data_enhanced_cnn',
                 since_date=None):
        self.db_path = db_path
        self.images_dir = images_dir
        self.since_date = since_date
        self.nabirds_clean_dir = nabirds_clean_dir
        self.unified_dir = unified_dir
        self.model = None
        self.class_names = None
        self.human_correction_timestamps = {}
        
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

        query = """
            SELECT species, image_path, timestamp FROM bird_visits 
            WHERE confidence = 1.0 
            AND species IS NOT NULL
            AND image_path IS NOT NULL
            AND species NOT IN ('Skip', 'Unknown Bird', 'Unknown; Not A Bird', 'Not A Bird', 'Poor Quality - Skipped')
        """
        params = []

        if self.since_date:
            query += " AND timestamp > ?"
            params.append(self.since_date)
            print(f"✅ Loading human corrections since {self.since_date}...")
        else:
            print("✅ Loading all human corrections from history...")

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return results

    def create_enhanced_dataset(self):
        """Create unified dataset: clean NABirds foundation + human corrections"""
        print("🔄 Creating enhanced dataset with human corrections...")

        # If unified directory is empty, initialize it with the NABirds foundation
        if not os.path.exists(self.unified_dir) or not any(Path(self.unified_dir).iterdir()):
            print("✨ Initializing new enhanced dataset...")
            if os.path.exists(self.unified_dir):
                shutil.rmtree(self.unified_dir)
            os.makedirs(self.unified_dir, exist_ok=True)

            print("📚 Copying clean NABirds foundation...")
            for species_dir in Path(self.nabirds_clean_dir).iterdir():
                if species_dir.is_dir():
                    dest_species_dir = Path(self.unified_dir) / species_dir.name
                    shutil.copytree(species_dir, dest_species_dir, dirs_exist_ok=True)
                    # Add 'nabirds_' prefix to all files for clear identification
                    for img_file in dest_species_dir.glob('*.jpg'):
                        if not img_file.name.startswith('nabirds_'):
                            img_file.rename(dest_species_dir / f"nabirds_{img_file.name}")
            print(f"✅ Foundation copied.")
        else:
            print("✅ Using existing enhanced dataset.")

        # Balancing parameters
        MAX_SAMPLES_PER_SPECIES = 150
        MIN_SAMPLES_PER_SPECIES = 20
        NABIRDS_PRESERVATION_RATIO = 0.4

        # Step 2: Add human corrections
        print(f"👥 Loading human corrections...")
        human_data = self.load_human_verified_data()
        if not human_data:
            print("No new human corrections to add.")
        else:
            print(f"Found {len(human_data)} new corrections to process.")

        human_stats = Counter()
        self.human_correction_timestamps = {}

        # Create a species name mapping from the unified directory itself
        species_mapping = {d.name.replace('_', ' '): d.name for d in Path(self.unified_dir).iterdir() if d.is_dir()}

        for species, image_path, timestamp in human_data:
            if not species or not image_path:
                continue

            if species not in species_mapping:
                print(f"✨ New species detected: {species}. Creating new directory.")
                nabirds_species_name = species.replace(' ', '_')
                dest_species_dir = Path(self.unified_dir) / nabirds_species_name
                dest_species_dir.mkdir(exist_ok=True)
                species_mapping[species] = nabirds_species_name
            else:
                nabirds_species_name = species_mapping[species]
                dest_species_dir = Path(self.unified_dir) / nabirds_species_name

            # Smart sample management
            current_files = list(dest_species_dir.glob("*.jpg"))
            if len(current_files) >= MAX_SAMPLES_PER_SPECIES:
                nabirds_files = [f for f in current_files if f.name.startswith('nabirds_')]
                human_files = [f for f in current_files if f.name.startswith('human_')]
                min_nabirds_to_keep = int(len(nabirds_files) * NABIRDS_PRESERVATION_RATIO)

                file_to_replace = None
                if len(nabirds_files) > min_nabirds_to_keep:
                    file_to_replace = min(nabirds_files, key=lambda f: f.stat().st_mtime)
                elif human_files:
                    file_to_replace = min(human_files, key=lambda f: f.stat().st_mtime)
                
                if file_to_replace:
                    print(f"🔄 {nabirds_species_name} at cap. Replacing oldest image: {file_to_replace.name}")
                    file_to_replace.unlink()
                else:
                    print(f"⚠️ {nabirds_species_name} at cap, but no replaceable image found. Skipping.")
                    continue

            try:
                resolved_path = self.resolve_image_path(image_path, species)
                if resolved_path.exists():
                    dest_filename = f"human_{resolved_path.name}"
                    dest_path = dest_species_dir / dest_filename
                    shutil.copy2(resolved_path, dest_path)
                    human_stats[nabirds_species_name] += 1
                    self.human_correction_timestamps[str(dest_path)] = timestamp
                else:
                    print(f"⚠️ Could not find image: {image_path} (resolved to: {resolved_path})")
            except Exception as e:
                print(f"⚠️ Failed to copy {image_path}: {e}")
        
        if sum(human_stats.values()) > 0:
            print(f"✅ Added {sum(human_stats.values())} new human corrections.")

        # Step 3: Generate final stats and prune
        print("\n📊 Generating final dataset summary...")
        final_stats = {}
        for species_dir in Path(self.unified_dir).iterdir():
            if not species_dir.is_dir(): continue
            count = len(list(species_dir.glob("*.jpg")))
            if count >= MIN_SAMPLES_PER_SPECIES:
                final_stats[species_dir.name] = count
            else:
                print(f"🗑️ Pruning {species_dir.name} - only {count} samples (min is {MIN_SAMPLES_PER_SPECIES}).")
                shutil.rmtree(species_dir)

        print(f"\nEnhanced Dataset Summary:")
        print(f"  Total Species: {len(final_stats)}")
        print(f"  Total Images: {sum(final_stats.values())}")

        for species, count in sorted(final_stats.items()):
            species_dir = Path(self.unified_dir) / species
            actual_human = len(list(species_dir.glob("human_*.jpg")))
            actual_nabirds = len(list(species_dir.glob("nabirds_*.jpg")))
            human_ratio = actual_human / count if count > 0 else 0
            status = "CAPPED" if count >= MAX_SAMPLES_PER_SPECIES else "OK"
            print(f"  - {species.replace('_', ' '):<25} | {count:>4} images | {human_ratio:.1%} human-verified [{status}]")

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
        y_pred = self.model.predict(val_generator, verbose=0)
        predicted_classes = np.argmax(y_pred, axis=1)
        
        # Extract true labels from the generator
        true_classes_list = []
        for i in range(len(val_generator)):
            _, y_batch, _ = val_generator[i] # Get the one-hot encoded labels
            true_classes_list.append(y_batch)
        true_classes_one_hot = np.concatenate(true_classes_list)
        true_classes = np.argmax(true_classes_one_hot, axis=1)

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
        
        # Extract true labels from the generator
        true_classes_list = []
        for i in range(len(val_generator)):
            _, y_batch, _ = val_generator[i] # Get the one-hot encoded labels
            true_classes_list.append(y_batch)
        true_classes_one_hot = np.concatenate(true_classes_list)
        true_classes = np.argmax(true_classes_one_hot, axis=1)
        
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
        
        # Manually collect all file paths and labels
        all_image_paths = []
        all_labels = []
        
        # Create a temporary generator to get class indices
        temp_gen = ImageDataGenerator().flow_from_directory(self.unified_dir, shuffle=False)
        self.class_names = list(temp_gen.class_indices.keys())
        class_indices = temp_gen.class_indices
        
        for species_dir in Path(self.unified_dir).iterdir():
            if species_dir.is_dir():
                species_name = species_dir.name
                label = class_indices[species_name]
                for img_path in species_dir.glob("*.jpg"):
                    all_image_paths.append(str(img_path))
                    all_labels.append(label)

        # Split data into training and validation sets
        from sklearn.model_selection import train_test_split
        train_paths, val_paths, train_labels, val_labels = train_test_split(
            all_image_paths, all_labels, test_size=0.2, random_state=42, stratify=all_labels
        )

        # Calculate class weights to handle imbalance
        class_weights = class_weight.compute_class_weight(
            'balanced',
            classes=np.unique(train_labels),
            y=train_labels
        )
        class_weights_dict = dict(enumerate(class_weights))
        print(f"⚖️ Applying combined sample and class weights to handle data imbalance and recency.")

        # Setup data augmentor for training
        train_augmentor = ImageDataGenerator(
            rotation_range=30,
            width_shift_range=0.25,
            height_shift_range=0.25,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.15,
            brightness_range=[0.8, 1.2]
        )

        # Create weighted generators, passing the class_weights_dict
        train_generator = WeightedDataGenerator(
            self.unified_dir, train_paths, train_labels, class_indices,
            self.batch_size, self.img_size, self.human_correction_timestamps,
            augmentor=train_augmentor, class_weights=class_weights_dict, shuffle=True, use_weights=True
        )
        
        val_generator = WeightedDataGenerator(
            self.unified_dir, val_paths, val_labels, class_indices,
            self.batch_size, self.img_size, self.human_correction_timestamps,
            augmentor=None, class_weights=class_weights_dict, shuffle=False, use_weights=False # No weights for validation
        )
        
        num_classes = len(self.class_names)
        
        print(f"✅ Training: {len(train_paths)}, Validation: {len(val_paths)}")
        
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
        print("🚀 Starting enhanced training with combined sample weights...")
        history = self.model.fit(
            train_generator,
            epochs=self.epochs,
            validation_data=val_generator,
            callbacks=callbacks,
            # REMOVED: class_weight=class_weights_dict,
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
            "total_training_samples": len(train_paths),
            "total_validation_samples": len(val_paths),
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
                "smart_sample_management_implemented",
                "sample_weighting_by_recency",
                "class_weighting_for_imbalance"
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
    parser = argparse.ArgumentParser(description='Enhanced CNN Bird Trainer')
    parser.add_argument('--since-date', type=str, default=None,
                        help='Only train on human corrections since this date (ISO format string).')
    args = parser.parse_args()

    trainer = EnhancedBirdTrainerCNN(since_date=args.since_date)
    metadata = trainer.train_enhanced_model()
    
    if metadata:
        print("\n✅ Enhanced CNN training successful!")
        print("🔄 Update custom_bird_classifier.py to use enhanced_nabirds_cnn.keras")

if __name__ == "__main__":
    main()
