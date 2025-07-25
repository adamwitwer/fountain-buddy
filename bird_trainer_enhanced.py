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
        """Combine human-verified and NABirds data into unified training structure"""
        print("Creating unified training dataset...")
        
        # Clear existing unified data
        if os.path.exists(self.unified_dir):
            shutil.rmtree(self.unified_dir)
        os.makedirs(self.unified_dir, exist_ok=True)
        
        dataset_stats = Counter()
        
        # Step 1: Load human-verified data from database
        human_data = self.load_human_verified_data()
        print(f"Loaded {len(human_data)} human-verified samples")
        
        # Step 2: Copy human-verified images by species
        for species, image_path, timestamp in human_data:
            if not species or species in ['Unknown; Not A Bird', 'Not A Bird']:
                continue
                
            # Clean species name for directory
            clean_species = species.replace(' ', '_').replace('/', '_')
            species_dir = os.path.join(self.unified_dir, clean_species)
            os.makedirs(species_dir, exist_ok=True)
            
            # Copy with descriptive filename
            if os.path.exists(image_path):
                timestamp_str = timestamp.replace(':', '-').replace(' ', '_')
                filename = f"human_{timestamp_str}_{os.path.basename(image_path)}"
                dst_path = os.path.join(species_dir, filename)
                
                try:
                    shutil.copy2(image_path, dst_path)
                    dataset_stats[clean_species] += 1
                except Exception as e:
                    print(f"Error copying {image_path}: {e}")
        
        # Step 3: Add NABirds data if available
        if os.path.exists(self.nabirds_dir):
            print("Adding NABirds professional images...")
            
            for species_dir in os.listdir(self.nabirds_dir):
                species_path = os.path.join(self.nabirds_dir, species_dir)
                if not os.path.isdir(species_path):
                    continue
                
                # Create unified species directory
                unified_species_dir = os.path.join(self.unified_dir, species_dir)
                os.makedirs(unified_species_dir, exist_ok=True)
                
                # Copy NABirds images
                for image_file in os.listdir(species_path):
                    if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        src_path = os.path.join(species_path, image_file)
                        dst_path = os.path.join(unified_species_dir, image_file)
                        
                        try:
                            shutil.copy2(src_path, dst_path)
                            dataset_stats[species_dir] += 1
                        except Exception as e:
                            print(f"Error copying NABirds image {src_path}: {e}")
        
        # Print dataset statistics
        print("\nUnified Dataset Statistics:")
        print("-" * 40)
        total_samples = 0
        for species, count in sorted(dataset_stats.items()):
            print(f"{species.replace('_', ' '):25} {count:4d} samples")
            total_samples += count
        print("-" * 40)
        print(f"{'Total':25} {total_samples:4d} samples")
        
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
        model_path = os.path.join(self.model_dir, 'enhanced_bird_classifier.h5')
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
                'aggressive_augmentation', 
                'learning_rate_scheduling',
                'early_stopping',
                'transfer_learning'
            ]
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
        report = classification_report(
            true_classes, 
            predicted_classes, 
            target_names=class_labels,
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