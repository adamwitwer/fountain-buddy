#!/usr/bin/env python3
"""
Test script to verify Fountain Buddy setup on Mac M4 Pro
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

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports...")
    
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} - GPU: {len(tf.config.list_physical_devices('GPU'))} devices")
    except Exception as e:
        print(f"❌ TensorFlow failed: {e}")
        return False
    
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__}")
    except Exception as e:
        print(f"❌ OpenCV failed: {e}")
        return False
    
    try:
        from ultralytics import YOLO
        print("✅ Ultralytics YOLO")
    except Exception as e:
        print(f"❌ Ultralytics failed: {e}")
        return False
    
    try:
        import discord
        print(f"✅ Discord.py {discord.__version__}")
    except Exception as e:
        print(f"❌ Discord.py failed: {e}")
        return False
    
    return True

def test_directories():
    """Test required directories"""
    print("\n📁 Testing directories...")
    
    import os
    required_dirs = [
        "bird_images",
        "training_data_unified", 
        "models",
        "memory-bank"
    ]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ exists")
        else:
            print(f"⚠️ {dir_name}/ missing (will be created when needed)")

def test_database():
    """Test database connectivity"""
    print("\n🗄️ Testing database...")
    
    import sqlite3
    import os
    
    if os.path.exists("fountain_buddy.db"):
        try:
            conn = sqlite3.connect("fountain_buddy.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM bird_visits")
            count = cursor.fetchone()[0]
            print(f"✅ Database connected - {count} bird visits recorded")
            conn.close()
        except Exception as e:
            print(f"⚠️ Database exists but has issues: {e}")
    else:
        print("⚠️ Database not found (copy from WSL2 or run --init-db)")

def main():
    print("🐦 Fountain Buddy Mac M4 Pro Setup Test")
    print("=" * 50)
    
    if test_imports():
        print("\n🎉 All imports successful!")
    else:
        print("\n❌ Some imports failed")
        return
    
    test_directories()
    test_database()
    
    print("\n📋 Next Steps:")
    print("1. Copy from WSL2:")
    print("   - .env file (camera and Discord settings)")
    print("   - fountain_buddy.db (your bird data)")
    print("   - training_data_unified/ directory (training images)")
    print("   - Any additional bird_images/ if needed")
    print("")
    print("2. Test training:")
    print("   python bird_trainer_enhanced.py")
    print("")
    print("3. Run the main application:")
    print("   python run.py")

if __name__ == "__main__":
    main()