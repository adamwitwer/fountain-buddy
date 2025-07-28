#!/usr/bin/env python3
"""
Optimized Custom CNN for Clean NABirds
Now that we know from-scratch training works, let's optimize for higher accuracy
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
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import json
from datetime import datetime
from pathlib import Path

# Configuration
NABIRDS_CLEAN_DIR = "nabirds_clean_training"
MODEL_OUTPUT_DIR = "models"
MODEL_NAME = "clean_nabirds_optimized_cnn.keras"
METADATA_NAME = "clean_nabirds_optimized_cnn_metadata.json"

# Optimized parameters
IMAGE_SIZE = (224, 224)  # Higher resolution for better accuracy
BATCH_SIZE = 16  # Smaller batch for stability
EPOCHS = 150
LEARNING_RATE = 0.001

def create_data_generators():
    """Create optimized data generators"""
    print("📂 Loading data for optimized CNN training...")
    
    # More aggressive augmentation since we know the model can learn
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
        NABIRDS_CLEAN_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        NABIRDS_CLEAN_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    return train_generator, val_generator

def create_optimized_cnn(num_classes):
    """Create deeper, optimized CNN"""
    print(f"🏗️ Creating optimized CNN for {num_classes} classes...")
    
    model = Sequential([
        # Block 1
        Conv2D(32, (3, 3), activation='relu', input_shape=(*IMAGE_SIZE, 3)),
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
        GlobalAveragePooling2D(),  # More robust than Flatten
        
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
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"📊 Total params: {model.count_params():,}")
    
    return model

def train_model():
    """Main training function for optimized CNN"""
    print("🚀 Optimized CNN Training (From Scratch)")
    print("=" * 50)
    print("Building on 52% success - targeting 80%+ accuracy")
    print("=" * 50)
    
    # Load data
    train_gen, val_gen = create_data_generators()
    
    class_names = list(train_gen.class_indices.keys())
    num_classes = len(class_names)
    
    print(f"✅ Found {num_classes} species")
    print(f"📊 Training: {train_gen.samples}, Validation: {val_gen.samples}")
    
    # Create model
    model = create_optimized_cnn(num_classes)
    
    # Optimized callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=25,  # More patience for better training
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.3,
            patience=10,
            min_lr=1e-8,
            verbose=1
        )
    ]
    
    # Train
    print("🚀 Starting optimized CNN training...")
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate
    val_loss, val_accuracy = model.evaluate(val_gen, verbose=0)
    print(f"✅ Final validation accuracy: {val_accuracy:.4f}")
    
    # Save model
    model_dir = Path(MODEL_OUTPUT_DIR)
    model_dir.mkdir(exist_ok=True)
    model_path = model_dir / MODEL_NAME
    model.save(model_path)
    
    # Save metadata
    metadata = {
        "model_path": str(model_path),
        "class_names": [name.replace('_', ' ') for name in class_names],
        "num_classes": num_classes,
        "image_size": list(IMAGE_SIZE),
        "training_date": datetime.now().isoformat(),
        "data_source": "nabirds_clean_balanced",
        "total_training_samples": train_gen.samples,
        "total_validation_samples": val_gen.samples,
        "training_history": {
            "final_accuracy": float(history.history['accuracy'][-1]),
            "final_val_accuracy": float(val_accuracy),
            "best_val_accuracy": float(max(history.history['val_accuracy'])),
            "epochs_completed": len(history.history['accuracy'])
        },
        "model_architecture": "Optimized Custom CNN (from scratch)",
        "improvements_over_simple": [
            "higher_resolution_224x224",
            "deeper_architecture_5_blocks",
            "global_average_pooling",
            "aggressive_augmentation",
            "dropout_regularization"
        ]
    }
    
    metadata_path = model_dir / METADATA_NAME
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"💾 Model saved: {model_path}")
    print(f"💾 Metadata saved: {metadata_path}")
    
    best_acc = max(history.history['val_accuracy'])
    print(f"\n🎉 Optimized CNN training complete!")
    print(f"📈 Best validation accuracy: {best_acc:.3f}")
    
    if best_acc > 0.8:
        print("🎯 EXCELLENT! Ready to replace the biased model!")
    elif best_acc > 0.6:
        print("✅ Good improvement! Much better than transfer learning!")
    else:
        print("🤔 Some improvement but may need more optimization")
    
    return metadata

if __name__ == "__main__":
    train_model()