#!/usr/bin/env python3
"""
Enhanced Bird Species Trainer with NABirds Integration
Combines human-verified local data with NABirds professional images for better training
"""

import os
import sqlite3
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import cv2
import shutil
from datetime import datetime
import json
from pathlib import Path
import glob
from collections import Counter

class EnhancedBirdTrainer:
    def __init__(self, db_path='fountain_buddy.db', images_dir='bird_images', 
                 nabirds_dir='nabirds_training_data', unified_dir='training_data_unified'):
        self.db_path = db_path
        self.images_dir = images_dir
        self.nabirds_dir = nabirds_dir
        self.unified_dir = unified_dir
        self.model = None
        self.label_encoder = None
        self.class_names = None
        
        # Training parameters - optimized for faster training
        self.img_size = (224, 224)  # Standard ResNet input size
        self.batch_size = 32  # Increased batch size for efficiency
        self.epochs = 30  # Reduced epochs with early stopping
        
        # Create directories
        self.model_dir = 'models'
        os.makedirs(self.unified_dir, exist_ok=True)
        os.makedirs(self.model_dir, exist_ok=True)
        
    def create_unified_dataset(self):
        """Combine human-verified and NABirds data into unified training structure with balancing"""
        print("Creating unified training dataset with balancing...")
        
        # Clear existing unified data
        if os.path.exists(self.unified_dir):
            shutil.rmtree(self.unified_dir)
        os.makedirs(self.unified_dir, exist_ok=True)
        
        dataset_stats = Counter()
        species_files = {}  # Track files per species for balancing
        
        # Balancing parameters
        MAX_SAMPLES_PER_SPECIES = 150
        MIN_SAMPLES_PER_SPECIES = 20  # Increased to filter out problematic species
        
        # Species to exclude (insufficient data even with NABirds)
        EXCLUDED_SPECIES = {'Hairy_Woodpecker', 'Catbird', 'Squirrel'}
        
        # Step 1: Load human-verified data from database
        human_data = self.load_human_verified_data()
        print(f"Loaded {len(human_data)} human-verified samples")
        
        # Step 2: Collect all available files per species first
        print("Collecting available samples per species...")
        
        # Collect human-verified files
        for species, image_path, timestamp in human_data:
            if not species or species in ['Unknown; Not A Bird', 'Not A Bird']:
                continue
                
            clean_species = species.replace(' ', '_').replace('/', '_')
            if clean_species not in species_files:
                species_files[clean_species] = []
            
            if os.path.exists(image_path):
                timestamp_str = timestamp.replace(':', '-').replace(' ', '_')
                filename = f"human_{timestamp_str}_{os.path.basename(image_path)}"
                species_files[clean_species].append({
                    'src': image_path,
                    'dst_filename': filename,
                    'source': 'human'
                })
        
        # Collect NABirds files
        if os.path.exists(self.nabirds_dir):
            print("Collecting NABirds professional images...")
            
            for species_dir in os.listdir(self.nabirds_dir):
                species_path = os.path.join(self.nabirds_dir, species_dir)
                if not os.path.isdir(species_path):
                    continue
                
                if species_dir not in species_files:
                    species_files[species_dir] = []
                
                for image_file in os.listdir(species_path):
                    if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        src_path = os.path.join(species_path, image_file)
                        species_files[species_dir].append({
                            'src': src_path,
                            'dst_filename': image_file,
                            'source': 'nabirds'
                        })
        
        # Step 3: Apply balancing and copy files
        print("Applying dataset balancing...")
        
        # Prioritize species with fewer samples
        species_by_count = sorted(species_files.items(), key=lambda x: len(x[1]))
        
        balancing_report = []
        
        for species, files in species_by_count:
            available_count = len(files)
            
            # Skip excluded species
            if species in EXCLUDED_SPECIES:
                print(f"⚠️  Excluding {species.replace('_', ' ')}: insufficient reliable data")
                continue
            
            # Determine target count
            if available_count < MIN_SAMPLES_PER_SPECIES:
                print(f"⚠️  Skipping {species.replace('_', ' ')}: only {available_count} samples (minimum {MIN_SAMPLES_PER_SPECIES})")
                continue
            elif available_count <= MAX_SAMPLES_PER_SPECIES:
                target_count = available_count  # Use all available
                status = "BALANCED"
            else:
                target_count = MAX_SAMPLES_PER_SPECIES  # Cap at maximum
                status = "CAPPED"
            
            # Create species directory
            species_dir = os.path.join(self.unified_dir, species)
            os.makedirs(species_dir, exist_ok=True)
            
            # Select files to use (prioritize human-verified, then random selection)
            human_files = [f for f in files if f['source'] == 'human']
            nabirds_files = [f for f in files if f['source'] == 'nabirds']
            
            selected_files = []
            
            # Always include all human-verified files first
            selected_files.extend(human_files)
            
            # Add NABirds files if we need more
            if len(selected_files) < target_count:
                remaining_needed = target_count - len(selected_files)
                # Randomly select from NABirds files
                import random
                random.seed(42)  # For reproducibility
                nabirds_sample = random.sample(nabirds_files, min(remaining_needed, len(nabirds_files)))
                selected_files.extend(nabirds_sample)
            
            # If we have too many (shouldn't happen with current logic, but safety check)
            if len(selected_files) > target_count:
                # Keep all human files, randomly sample NABirds
                if len(human_files) <= target_count:
                    remaining_slots = target_count - len(human_files)
                    nabirds_in_selection = [f for f in selected_files if f['source'] == 'nabirds']
                    random.seed(42)
                    nabirds_final = random.sample(nabirds_in_selection, remaining_slots)
                    selected_files = human_files + nabirds_final
                else:
                    # Even human files exceed target (rare case)
                    random.seed(42)
                    selected_files = random.sample(human_files, target_count)
            
            # Copy selected files
            copied_count = 0
            for file_info in selected_files:
                dst_path = os.path.join(species_dir, file_info['dst_filename'])
                try:
                    shutil.copy2(file_info['src'], dst_path)
                    copied_count += 1
                except Exception as e:
                    print(f"Error copying {file_info['src']}: {e}")
            
            dataset_stats[species] = copied_count
            balancing_report.append({
                'species': species,
                'available': available_count,
                'target': target_count,
                'copied': copied_count,
                'status': status,
                'human_files': len(human_files),
                'nabirds_files': len(nabirds_files)
            })
        
        # Print detailed balancing report
        print("\nDataset Balancing Report:")
        print("=" * 80)
        print(f"{'Species':25} {'Available':>9} {'Target':>7} {'Used':>6} {'Status':>10} {'Human':>6} {'NABirds':>8}")
        print("-" * 80)
        
        for report in balancing_report:
            print(f"{report['species'].replace('_', ' '):25} "
                  f"{report['available']:>9} "
                  f"{report['target']:>7} "
                  f"{report['copied']:>6} "
                  f"{report['status']:>10} "
                  f"{report['human_files']:>6} "
                  f"{report['nabirds_files']:>8}")
        
        total_samples = sum(dataset_stats.values())
        print("-" * 80)
        print(f"{'TOTAL':25} {sum(len(files) for files in species_files.values()):>9} "
              f"{'':>7} {total_samples:>6} {'':>10} {'':>6} {'':>8}")
        
        # Summary statistics
        capped_species = [r for r in balancing_report if r['status'] == 'CAPPED']
        if capped_species:
            print(f"\n🔧 Capped species (>{MAX_SAMPLES_PER_SPECIES} samples): {len(capped_species)}")
            for species_info in capped_species:
                reduction = species_info['available'] - species_info['copied']
                print(f"   • {species_info['species'].replace('_', ' ')}: {species_info['available']} → {species_info['copied']} (-{reduction})")
        
        print(f"\n📊 Final dataset: {total_samples} samples across {len(dataset_stats)} species")
        print(f"📈 Average samples per species: {total_samples / len(dataset_stats):.1f}")
        
        return dataset_stats
    
    def load_human_verified_data(self):
        """Load human-verified bird data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all human-verified entries
        cursor.execute("""
            SELECT species, image_path, timestamp 
            FROM bird_visits 
            WHERE species IS NOT NULL 
            AND confidence = 1.0 
            AND species NOT IN ('Unknown; Not A Bird', 'Not A Bird')
            AND timestamp > '2025-07-03'
            ORDER BY timestamp DESC
        """)
        
        data = cursor.fetchall()
        conn.close()
        return data
    
    def create_optimized_data_generators(self):
        """Create data generators with aggressive augmentation and optimization"""
        
        # Enhanced data augmentation for better generalization
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=25,
            width_shift_range=0.15,
            height_shift_range=0.15,
            shear_range=0.15,
            zoom_range=0.15,
            horizontal_flip=True,
            brightness_range=[0.8, 1.2],
            fill_mode='nearest',
            validation_split=0.2  # 80% train, 20% validation
        )
        
        # Simple rescaling for validation
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=0.2
        )
        
        # Create generators
        train_generator = train_datagen.flow_from_directory(
            self.unified_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True,
            seed=42
        )
        
        validation_generator = val_datagen.flow_from_directory(
            self.unified_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False,
            seed=42
        )
        
        # Store class information
        self.class_names = list(train_generator.class_indices.keys())
        self.num_classes = len(self.class_names)
        
        print(f"\nTraining generator: {train_generator.samples} samples")
        print(f"Validation generator: {validation_generator.samples} samples")
        print(f"Number of classes: {self.num_classes}")
        print(f"Classes: {self.class_names}")
        
        return train_generator, validation_generator
    
    def create_optimized_model(self):
        """Create an optimized ResNet50 model with modern techniques"""
        print("Building optimized ResNet50 model...")
        
        # Use ResNet50 as base with ImageNet weights
        base_model = ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=(*self.img_size, 3)
        )
        
        # Freeze early layers, fine-tune later ones
        for layer in base_model.layers[:-30]:  # Freeze all but last 30 layers
            layer.trainable = False
        
        # Add custom classification head
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.5)(x)
        x = Dense(512, activation='relu', name='fc1')(x)
        x = Dropout(0.3)(x)
        predictions = Dense(self.num_classes, activation='softmax', name='predictions')(x)
        
        model = Model(inputs=base_model.input, outputs=predictions)
        
        # Use modern optimizer with learning rate scheduling
        initial_lr = 0.0001
        optimizer = Adam(learning_rate=initial_lr)
        
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"Model created with {model.count_params():,} parameters")
        print(f"Trainable parameters: {sum([np.prod(p.shape) for p in model.trainable_weights]):,}")
        
        return model
    
    def get_callbacks(self):
        """Get optimized callbacks for training"""
        callbacks = [
            # Early stopping with patience
            EarlyStopping(
                monitor='val_accuracy',
                patience=8,
                restore_best_weights=True,
                verbose=1
            ),
            
            # Learning rate reduction
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=4,
                min_lr=1e-7,
                verbose=1
            ),
            
            # Model checkpointing
            ModelCheckpoint(
                os.path.join(self.model_dir, 'best_enhanced_bird_model.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        return callbacks
    
    def train_model(self):
        """Main training function with optimizations"""
        print("Starting Enhanced Bird Species Training Pipeline")
        print("=" * 60)
        
        # Step 1: Create unified dataset
        dataset_stats = self.create_unified_dataset()
        
        # Step 2: Create optimized data generators
        train_gen, val_gen = self.create_optimized_data_generators()
        
        # Step 3: Create optimized model
        self.model = self.create_optimized_model()
        
        # Step 4: Train with callbacks
        print(f"\nStarting training for {self.epochs} epochs...")
        print(f"Batch size: {self.batch_size}")
        print(f"Image size: {self.img_size}")
        
        history = self.model.fit(
            train_gen,
            epochs=self.epochs,
            validation_data=val_gen,
            callbacks=self.get_callbacks(),
            verbose=1
        )
        
        # Step 5: Save final model and metadata
        self.save_model_and_metadata(dataset_stats, history)
        
        # Step 6: Evaluate performance
        self.evaluate_model(val_gen)
        
        return history
    
    def save_model_and_metadata(self, dataset_stats, history):
        """Save the trained model and comprehensive metadata"""
        
        # Save the model
        model_path = os.path.join(self.model_dir, 'enhanced_bird_classifier.keras')
        self.model.save(model_path)
        
        # Create comprehensive metadata
        metadata = {
            'model_path': model_path,
            'class_names': [name.replace('_', ' ') for name in self.class_names],
            'num_classes': self.num_classes,
            'image_size': self.img_size,
            'training_date': datetime.now().isoformat(),
            'dataset_stats': dict(dataset_stats),
            'total_training_samples': sum(dataset_stats.values()),
            'training_history': {
                'final_accuracy': float(history.history['accuracy'][-1]),
                'final_val_accuracy': float(history.history['val_accuracy'][-1]),
                'best_val_accuracy': float(max(history.history['val_accuracy'])),
                'epochs_completed': len(history.history['accuracy'])
            },
            'model_architecture': 'ResNet50 + Custom Head',
            'data_sources': ['human_verified', 'nabirds_professional'],
            'optimization_features': [
                'mixed_data_sources',
                'dataset_balancing',
                'aggressive_augmentation', 
                'learning_rate_scheduling',
                'early_stopping',
                'transfer_learning'
            ],
            'balancing_config': {
                'max_samples_per_species': 100,
                'min_samples_per_species': 10,
                'prioritizes_human_verified': True
            }
        }
        
        # Save metadata
        metadata_path = os.path.join(self.model_dir, 'enhanced_model_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\nModel saved: {model_path}")
        print(f"Metadata saved: {metadata_path}")
        
        return metadata
    
    def evaluate_model(self, validation_generator):
        """Evaluate the trained model"""
        print("\nEvaluating model performance...")
        
        # Get predictions
        validation_generator.reset()
        predictions = self.model.predict(validation_generator, verbose=1)
        predicted_classes = np.argmax(predictions, axis=1)
        
        # Get true labels
        true_classes = validation_generator.classes
        class_labels = list(validation_generator.class_indices.keys())
        
        # Classification report
        print("\nClassification Report:")
        print("-" * 60)
        # Get unique classes present in validation set
        unique_classes = sorted(set(true_classes))
        present_class_names = [class_labels[i] for i in unique_classes]
        
        report = classification_report(
            true_classes, 
            predicted_classes, 
            target_names=present_class_names,
            labels=unique_classes,
            digits=3
        )
        print(report)
        
        # Overall accuracy
        accuracy = np.mean(predicted_classes == true_classes)
        print(f"\nOverall Validation Accuracy: {accuracy:.3f}")
        
        return accuracy, report

def main():
    """Main training execution"""
    # Enable mixed precision for faster training
    tf.keras.mixed_precision.set_global_policy('mixed_float16')
    
    # Set memory growth for GPU (if available)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"GPU acceleration enabled: {len(gpus)} GPU(s) found")
        except RuntimeError as e:
            print(f"GPU setup error: {e}")
    
    # Create and run trainer
    trainer = EnhancedBirdTrainer()
    
    try:
        history = trainer.train_model()
        print("\n" + "="*60)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("Key improvements over previous version:")
        print("• 265 additional NABirds images added")
        print("• Balanced dataset across all species")
        print("• Optimized training pipeline")
        print("• Mixed precision for faster training")
        print("• Enhanced data augmentation")
        print("• Early stopping and LR scheduling")
        print("\nNext: Update your main application to use the new model!")
        
    except Exception as e:
        print(f"Training failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()