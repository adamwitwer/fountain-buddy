#!/usr/bin/env python3
"""
Unified Bird Species Trainer for 19-class model.
Supports both fountain and peanut feeder species in a single classifier.
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
from species_mapping import UNIFIED_SPECIES_LIST, generate_metadata

class UnifiedBirdTrainer:
    def __init__(self, training_dir='training_data_unified', model_dir='models'):
        self.training_dir = training_dir
        self.model_dir = model_dir
        self.model = None
        self.label_encoder = None
        self.class_names = UNIFIED_SPECIES_LIST
        
        # Create directories
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Model configuration
        self.img_size = (224, 224)
        self.batch_size = 32
        self.epochs = 50
        self.num_classes = len(UNIFIED_SPECIES_LIST)
        
        print(f"🤖 Initialized trainer for {self.num_classes} species")
        
    def analyze_training_data(self):
        """Analyze the available training data."""
        
        print("🔍 Analyzing training data...")
        
        if not os.path.exists(self.training_dir):
            print(f"❌ Training directory not found: {self.training_dir}")
            return {}
        
        species_data = {}
        total_images = 0
        
        for species_name in self.class_names:
            species_dir = os.path.join(self.training_dir, species_name.replace(' ', '_'))
            
            if os.path.exists(species_dir):
                image_files = [f for f in os.listdir(species_dir) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                count = len(image_files)
                species_data[species_name] = count
                total_images += count
                
                status = "🟢 Ready" if count >= 20 else "🟡 Few" if count >= 5 else "🔴 Missing"
                print(f"   {species_name:25}: {count:3d} images {status}")
            else:
                species_data[species_name] = 0
                print(f"   {species_name:25}:   0 images 🔴 Missing")
        
        ready_count = sum(1 for count in species_data.values() if count >= 20)
        few_count = sum(1 for count in species_data.values() if 5 <= count < 20)
        missing_count = sum(1 for count in species_data.values() if count < 5)
        
        print(f"\n📊 Summary:")
        print(f"   Total images: {total_images}")
        print(f"   Ready species (≥20): {ready_count}")
        print(f"   Few data (5-19): {few_count}")
        print(f"   Missing data (<5): {missing_count}")
        
        return species_data
    
    def prepare_data_generators(self, validation_split=0.2):
        """Prepare data generators for training."""
        
        print("📊 Preparing data generators...")
        
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            validation_split=validation_split
        )
        
        # Only rescaling for validation
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=validation_split
        )
        
        # Training generator
        train_generator = train_datagen.flow_from_directory(
            self.training_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        # Validation generator
        validation_generator = val_datagen.flow_from_directory(
            self.training_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        # Store class indices mapping
        self.class_indices = train_generator.class_indices
        self.index_to_class = {v: k for k, v in self.class_indices.items()}
        
        print(f"✅ Training samples: {train_generator.samples}")
        print(f"✅ Validation samples: {validation_generator.samples}")
        print(f"✅ Found {len(self.class_indices)} classes")
        
        return train_generator, validation_generator
    
    def build_model(self):
        """Build the unified bird classification model."""
        
        print("🏗️ Building unified bird classification model...")
        
        # Load pre-trained ResNet50
        base_model = ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=(*self.img_size, 3)
        )
        
        # Freeze base model layers initially
        base_model.trainable = False
        
        # Add custom classification head
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        predictions = Dense(self.num_classes, activation='softmax')(x)
        
        # Create the model
        self.model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile the model
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"✅ Model built with {self.num_classes} output classes")
        print(f"   Total parameters: {self.model.count_params():,}")
        
        return self.model
    
    def train_model(self, train_generator, validation_generator):
        """Train the unified bird classification model."""
        
        print("🚀 Starting model training...")
        
        # Calculate steps per epoch
        steps_per_epoch = train_generator.samples // self.batch_size
        validation_steps = validation_generator.samples // self.batch_size
        
        # Define callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            ModelCheckpoint(
                os.path.join(self.model_dir, 'best_unified_bird_model.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Phase 1: Train with frozen base model
        print("📚 Phase 1: Training classification head...")
        history_phase1 = self.model.fit(
            train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=min(15, self.epochs // 3),
            validation_data=validation_generator,
            validation_steps=validation_steps,
            callbacks=callbacks,
            verbose=1
        )
        
        # Phase 2: Fine-tune some layers
        print("🔧 Phase 2: Fine-tuning top layers...")
        
        # Unfreeze top layers of base model
        base_model = self.model.layers[0]
        base_model.trainable = True
        
        # Fine-tune from this layer onwards
        fine_tune_at = len(base_model.layers) - 30
        
        # Freeze all layers before fine_tune_at
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Continue training
        history_phase2 = self.model.fit(
            train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=self.epochs - min(15, self.epochs // 3),
            initial_epoch=min(15, self.epochs // 3),
            validation_data=validation_generator,
            validation_steps=validation_steps,
            callbacks=callbacks,
            verbose=1
        )
        
        # Combine histories
        history = {
            'loss': history_phase1.history['loss'] + history_phase2.history['loss'],
            'accuracy': history_phase1.history['accuracy'] + history_phase2.history['accuracy'],
            'val_loss': history_phase1.history['val_loss'] + history_phase2.history['val_loss'],
            'val_accuracy': history_phase1.history['val_accuracy'] + history_phase2.history['val_accuracy']
        }
        
        return history
    
    def evaluate_model(self, validation_generator):
        """Evaluate the trained model."""
        
        print("📊 Evaluating model performance...")
        
        # Load best model
        best_model_path = os.path.join(self.model_dir, 'best_unified_bird_model.h5')
        if os.path.exists(best_model_path):
            self.model = tf.keras.models.load_model(best_model_path)
            print("✅ Loaded best model for evaluation")
        
        # Evaluate on validation set
        loss, accuracy = self.model.evaluate(validation_generator, verbose=0)
        print(f"📈 Validation accuracy: {accuracy:.4f}")
        print(f"📉 Validation loss: {loss:.4f}")
        
        # Generate predictions for detailed analysis
        validation_generator.reset()
        predictions = self.model.predict(validation_generator, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)
        
        true_classes = validation_generator.classes
        class_labels = list(validation_generator.class_indices.keys())
        
        # Classification report
        print("\n📋 Classification Report:")
        print(classification_report(true_classes, predicted_classes, target_names=class_labels))
        
        return {
            'accuracy': accuracy,
            'loss': loss,
            'predictions': predictions,
            'true_classes': true_classes,
            'predicted_classes': predicted_classes
        }
    
    def save_model(self, training_samples_count):
        """Save the final model and metadata."""
        
        print("💾 Saving unified model...")
        
        # Save model
        model_path = os.path.join(self.model_dir, 'fountain_buddy_unified_classifier.h5')
        self.model.save(model_path)
        
        # Generate and save metadata
        metadata = generate_metadata()
        metadata.update({
            'trained_on': datetime.now().isoformat(),
            'training_samples': training_samples_count,
            'model_architecture': 'ResNet50 + Custom Head',
            'input_shape': [*self.img_size, 3],
            'model_file': 'fountain_buddy_unified_classifier.h5'
        })
        
        metadata_path = os.path.join(self.model_dir, 'unified_model_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Model saved: {model_path}")
        print(f"✅ Metadata saved: {metadata_path}")
        
        return model_path, metadata_path
    
    def train_unified_model(self):
        """Complete training pipeline for unified model."""
        
        print("🚀 Starting Unified Bird Classifier Training")
        print("=" * 60)
        
        # Step 1: Analyze data
        species_data = self.analyze_training_data()
        
        # Check if we have enough data
        ready_species = sum(1 for count in species_data.values() if count >= 5)
        if ready_species < 8:
            print(f"❌ Insufficient training data. Only {ready_species} species have ≥5 images.")
            print("   Need at least 8 species with sufficient data to train.")
            return False
        
        total_samples = sum(species_data.values())
        print(f"📊 Training with {ready_species} species, {total_samples} total images")
        
        # Step 2: Prepare data
        train_gen, val_gen = self.prepare_data_generators()
        
        # Step 3: Build model
        self.build_model()
        
        # Step 4: Train model
        history = self.train_model(train_gen, val_gen)
        
        # Step 5: Evaluate model
        results = self.evaluate_model(val_gen)
        
        # Step 6: Save model
        model_path, metadata_path = self.save_model(total_samples)
        
        # Step 7: Training summary
        print(f"\n🎉 Training Complete!")
        print(f"✅ Final accuracy: {results['accuracy']:.4f}")
        print(f"✅ Model saved: {model_path}")
        print(f"✅ Species supported: {len(self.class_names)}")
        
        return True

def main():
    """Main training function."""
    
    # Initialize trainer
    trainer = UnifiedBirdTrainer()
    
    # Run training
    success = trainer.train_unified_model()
    
    if success:
        print("\n🚀 Next steps:")
        print("1. Update custom_bird_classifier.py to use new unified model")
        print("2. Test model with both fountain and peanut camera detections")
        print("3. Continue collecting data for missing species")
    else:
        print("\n⚠️ Training not completed. Collect more training data first.")

if __name__ == "__main__":
    main()