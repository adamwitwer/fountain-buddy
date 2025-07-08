#!/usr/bin/env python3
"""
Bird Species Fine-tuning Pipeline
Transfer learning approach to improve ResNet-50 accuracy using human corrections
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

class BirdSpeciesTrainer:
    def __init__(self, db_path='fountain_buddy.db', images_dir='bird_images'):
        self.db_path = db_path
        self.images_dir = images_dir
        self.model = None
        self.label_encoder = None
        self.class_names = None
        
        # Create training directories
        self.train_dir = 'training_data'
        self.model_dir = 'models'
        os.makedirs(self.train_dir, exist_ok=True)
        os.makedirs(self.model_dir, exist_ok=True)
        
    def load_human_verified_data(self):
        """Load human-verified bird data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all human-verified entries with reliable data (July 3+)
        cursor.execute("""
            SELECT species, image_path, timestamp 
            FROM bird_visits 
            WHERE species IS NOT NULL 
            AND confidence = 1.0 
            AND species NOT IN ('Unknown; Not A Bird', 'Not A Bird')
            AND timestamp >= '2025-07-03'
        """)
        
        data = cursor.fetchall()
        conn.close()
        
        print(f"Found {len(data)} human-verified bird records")
        
        # Group by species and show distribution
        species_counts = {}
        for species, _, _ in data:
            species_counts[species] = species_counts.get(species, 0) + 1
        
        print("\nSpecies distribution:")
        for species, count in sorted(species_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {species}: {count}")
        
        return data
    
    def prepare_training_data(self, data):
        """Organize images into training directory structure"""
        # Clear existing training data
        if os.path.exists(self.train_dir):
            shutil.rmtree(self.train_dir)
        os.makedirs(self.train_dir)
        
        # Create species subdirectories and copy images
        valid_data = []
        for species, image_path, timestamp in data:
            species_dir = os.path.join(self.train_dir, species.replace(' ', '_'))
            os.makedirs(species_dir, exist_ok=True)
            
            # Find the actual image file
            image_file = None
            if image_path and os.path.exists(image_path):
                image_file = image_path
            else:
                # Try to find by timestamp
                timestamp_str = timestamp.replace(':', '-').replace(' ', '_')
                possible_files = [
                    f"bird_{timestamp_str}.jpg",
                    f"bird_{species.replace(' ', '_')}_{timestamp_str}.jpg"
                ]
                
                for possible_file in possible_files:
                    full_path = os.path.join(self.images_dir, possible_file)
                    if os.path.exists(full_path):
                        image_file = full_path
                        break
                
                # Try finding by date pattern
                if not image_file:
                    date_part = timestamp.split(' ')[0]
                    for file in os.listdir(self.images_dir):
                        if date_part in file:
                            image_file = os.path.join(self.images_dir, file)
                            break
            
            if image_file and os.path.exists(image_file):
                dest_file = os.path.join(species_dir, f"{species.replace(' ', '_')}_{len(valid_data)}.jpg")
                shutil.copy2(image_file, dest_file)
                valid_data.append((species, dest_file))
            else:
                print(f"Warning: Could not find image for {species} at {timestamp}")
        
        print(f"\nPrepared {len(valid_data)} images for training")
        return valid_data
    
    def create_model(self, num_classes):
        """Create fine-tuned ResNet-50 model"""
        # Load pre-trained ResNet-50
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        
        # Freeze early layers, allow fine-tuning of last few layers
        for layer in base_model.layers[:-10]:
            layer.trainable = False
        
        # Add custom classification head
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        predictions = Dense(num_classes, activation='softmax')(x)
        
        model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile with lower learning rate for fine-tuning
        model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_model(self, data):
        """Train the bird species classifier"""
        # Prepare data
        species_list = [item[0] for item in data]
        self.label_encoder = LabelEncoder()
        encoded_labels = self.label_encoder.fit_transform(species_list)
        self.class_names = self.label_encoder.classes_
        
        print(f"\nTraining on {len(self.class_names)} species:")
        for i, species in enumerate(self.class_names):
            count = np.sum(encoded_labels == i)
            print(f"  {species}: {count} samples")
        
        # Create data generators
        datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            fill_mode='nearest',
            validation_split=0.2
        )
        
        # Training generator
        train_generator = datagen.flow_from_directory(
            self.train_dir,
            target_size=(224, 224),
            batch_size=16,
            class_mode='categorical',
            subset='training'
        )
        
        # Validation generator
        validation_generator = datagen.flow_from_directory(
            self.train_dir,
            target_size=(224, 224),
            batch_size=16,
            class_mode='categorical',
            subset='validation'
        )
        
        # Create model
        self.model = self.create_model(len(self.class_names))
        
        # Callbacks
        callbacks = [
            EarlyStopping(patience=10, restore_best_weights=True),
            ReduceLROnPlateau(factor=0.5, patience=5),
            ModelCheckpoint(
                os.path.join(self.model_dir, 'best_bird_model.h5'),
                save_best_only=True
            )
        ]
        
        # Train model
        history = self.model.fit(
            train_generator,
            epochs=50,
            validation_data=validation_generator,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def save_model(self):
        """Save the trained model and metadata"""
        if self.model is None:
            raise ValueError("No model to save")
        
        # Save model
        model_path = os.path.join(self.model_dir, 'fountain_buddy_bird_classifier.h5')
        self.model.save(model_path)
        
        # Save class names and metadata
        # Count total training samples across all species directories
        total_samples = 0
        for species_dir in os.listdir(self.train_dir):
            species_path = os.path.join(self.train_dir, species_dir)
            if os.path.isdir(species_path):
                total_samples += len(os.listdir(species_path))
        
        metadata = {
            'class_names': self.class_names.tolist(),
            'num_classes': len(self.class_names),
            'trained_on': datetime.now().isoformat(),
            'training_samples': total_samples
        }
        
        metadata_path = os.path.join(self.model_dir, 'model_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\nModel saved to: {model_path}")
        print(f"Metadata saved to: {metadata_path}")
        print(f"Training samples recorded: {total_samples}")
        
        # Verify metadata was saved correctly
        with open(metadata_path, 'r') as f:
            saved_metadata = json.load(f)
        
        if saved_metadata['training_samples'] != total_samples:
            print(f"WARNING: Metadata mismatch! Expected {total_samples}, got {saved_metadata['training_samples']}")
        else:
            print("✅ Metadata verification passed")
        
        return model_path, metadata_path
    
    def evaluate_model(self):
        """Evaluate the trained model"""
        if self.model is None:
            raise ValueError("No model to evaluate")
        
        # Create test generator
        test_datagen = ImageDataGenerator(rescale=1./255)
        test_generator = test_datagen.flow_from_directory(
            self.train_dir,
            target_size=(224, 224),
            batch_size=1,
            class_mode='categorical',
            shuffle=False
        )
        
        # Make predictions
        predictions = self.model.predict(test_generator)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = test_generator.classes
        
        # Print evaluation metrics
        print("\nModel Evaluation:")
        print("="*50)
        print(classification_report(true_classes, predicted_classes, 
                                  target_names=self.class_names))
        
        return predictions, true_classes, predicted_classes

def main():
    """Main training pipeline"""
    print("Starting Bird Species Fine-tuning Pipeline")
    print("="*50)
    
    trainer = BirdSpeciesTrainer()
    
    # Load human-verified data
    data = trainer.load_human_verified_data()
    
    if len(data) < 10:
        print("Not enough training data. Need at least 10 human-verified samples.")
        return
    
    # Prepare training data
    valid_data = trainer.prepare_training_data(data)
    
    if len(valid_data) < 10:
        print("Not enough valid images found. Check image paths.")
        return
    
    # Train model
    history = trainer.train_model(valid_data)
    
    # Save model
    trainer.save_model()
    
    # Evaluate model
    trainer.evaluate_model()
    
    print("\nTraining completed successfully!")
    print("You can now use the trained model in your fountain monitoring system.")

if __name__ == "__main__":
    main()