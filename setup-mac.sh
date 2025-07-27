#!/bin/bash
# Mac M4 Pro setup script for Fountain Buddy

echo "🐦 Setting up Fountain Buddy on Mac M4 Pro..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Please activate your virtual environment first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    exit 1
fi

echo "✅ Virtual environment detected: $VIRTUAL_ENV"

# Update pip first
echo "📦 Updating pip..."
pip install --upgrade pip

# Install Mac-optimized dependencies
echo "🔧 Installing Mac-optimized dependencies..."
pip install -r requirements-mac.txt

# Verify TensorFlow installation
echo "🧠 Verifying TensorFlow installation..."
python3 -c "
import tensorflow as tf
print(f'TensorFlow version: {tf.__version__}')
print(f'Metal GPU available: {len(tf.config.list_physical_devices(\"GPU\")) > 0}')
print(f'CPU devices: {len(tf.config.list_physical_devices(\"CPU\"))}')
"

# Test OpenCV
echo "👁️ Testing OpenCV..."
python3 -c "
import cv2
print(f'OpenCV version: {cv2.__version__}')
"

# Test Ultralytics
echo "🎯 Testing YOLO/Ultralytics..."
python3 -c "
from ultralytics import YOLO
print('✅ Ultralytics/YOLO imported successfully')
"

echo "🎉 Setup complete! Your Mac M4 Pro is ready for bird training."
echo ""
echo "Next steps:"
echo "1. Copy your .env file and database from WSL2"
echo "2. Run: python3 run.py --init-db (if needed)"
echo "3. Start training: python3 bird_trainer_enhanced.py"