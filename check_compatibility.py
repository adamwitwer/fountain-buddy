#!/usr/bin/env python3
"""
Mac M4 Pro Python 3.13 compatibility checker for Fountain Buddy
Run this before main installation to identify potential issues
"""

import sys
import platform
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3:
        print("❌ Python 3 required")
        return False
    
    if version.minor < 8:
        print("❌ Python 3.8+ required")
        return False
    
    if version.minor >= 13:
        print("⚠️ Python 3.13 detected - some packages may need special handling")
    
    print("✅ Python version compatible")
    return True

def check_platform():
    """Check if we're on Apple Silicon Mac"""
    machine = platform.machine()
    system = platform.system()
    
    print(f"💻 Platform: {system} {machine}")
    
    if system != "Darwin":
        print("❌ This script is for macOS only")
        return False
    
    if machine != "arm64":
        print("⚠️ Not Apple Silicon - may need Intel-specific packages")
    else:
        print("✅ Apple Silicon detected")
    
    return True

def check_homebrew():
    """Check if Homebrew is available"""
    try:
        result = subprocess.run(["brew", "--version"], 
                              capture_output=True, text=True, check=True)
        print("✅ Homebrew available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Homebrew not found - some packages may fail")
        print("   Install: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        return False

def check_xcode():
    """Check if Xcode command line tools are available"""
    try:
        result = subprocess.run(["xcode-select", "--print-path"], 
                              capture_output=True, text=True, check=True)
        print("✅ Xcode command line tools available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Xcode command line tools required")
        print("   Install: xcode-select --install")
        return False

def main():
    print("🔍 Checking Mac M4 Pro compatibility for Fountain Buddy...\n")
    
    checks = [
        check_python_version(),
        check_platform(),
        check_homebrew(),
        check_xcode()
    ]
    
    print(f"\n📊 Compatibility check: {sum(checks)}/4 passed")
    
    if all(checks):
        print("🎉 All checks passed! Ready to install dependencies.")
        print("\nNext step: source venv/bin/activate && ./setup-mac.sh")
    else:
        print("⚠️ Some issues detected. Address them before continuing.")

if __name__ == "__main__":
    main()