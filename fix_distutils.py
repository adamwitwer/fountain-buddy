#!/usr/bin/env python3
"""
Compatibility fix for Python 3.12 distutils removal
Run this before importing TensorFlow
"""

import sys
import warnings

# Suppress the deprecation warning about distutils
warnings.filterwarnings("ignore", category=DeprecationWarning, module="distutils")

try:
    import distutils
except ImportError:
    # Create a minimal distutils replacement for TensorFlow compatibility
    import importlib.util
    from unittest.mock import MagicMock
    
    # Create the distutils module mock
    distutils_spec = importlib.util.spec_from_loader("distutils", loader=None)
    distutils_module = importlib.util.module_from_spec(distutils_spec)
    
    # Add minimal required components that TensorFlow uses
    distutils_module.version = MagicMock()
    distutils_module.spawn = MagicMock()
    distutils_module.util = MagicMock()
    
    # Install the mock module
    sys.modules["distutils"] = distutils_module
    sys.modules["distutils.version"] = distutils_module.version
    sys.modules["distutils.spawn"] = distutils_module.spawn
    sys.modules["distutils.util"] = distutils_module.util
    
    print("✅ Applied distutils compatibility fix for Python 3.12")