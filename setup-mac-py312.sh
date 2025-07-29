#!/bin/bash
# Mac M4 Pro setup script for Fountain Buddy with Python 3.12

echo "🐦 Setting up Fountain Buddy on Mac M4 Pro with Python 3.12..."

# Remove existing venv if it exists
if [ -d "venv" ]; then
    echo "🗑️ Removing existing Python 3.13 virtual environment..."
    rm -rf venv
fi

# Create new venv with Python 3.12
echo "🐍 Creating virtual environment with Python 3.12..."
/opt/homebrew/bin/python3.12 -m venv venv

# Activate the environment
source venv/bin/activate

echo "✅ Virtual environment created with Python $(python --version)"

# Update pip first
echo "📦 Updating pip..."
pip install --upgrade pip

# Install Mac-optimized dependencies
echo "🔧 Installing Mac-optimized dependencies..."
pip install -r requirements-mac.txt

# Verify installations
echo "🧠 Verifying TensorFlow installation..."
python -c "
import tensorflow as tf
print(f'TensorFlow version: {tf.__version__}')
print(f'GPU devices: {len(tf.config.list_physical_devices(\"GPU\"))}')
print(f'CPU devices: {len(tf.config.list_physical_devices(\"CPU\"))}')
"

echo "👁️ Testing OpenCV..."
python -c "
import cv2
print(f'OpenCV version: {cv2.__version__}')
"

echo "🎯 Testing YOLO/Ultralytics..."
python -c "
from ultralytics import YOLO
print('✅ Ultralytics/YOLO imported successfully')
"

echo "🎉 Setup complete! Your Mac M4 Pro is ready for bird training."
echo ""
echo "⚠️ Remember to use Python 3.12 environment:"
echo "   source venv/bin/activate"