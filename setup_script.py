#!/usr/bin/env python3
"""
🔧 Setup Script for Vulnerable LLM Research Environment 🔧

This script helps set up the vulnerable LLM environment for research purposes.
It installs dependencies, checks system requirements, and provides setup guidance.

⚠️ WARNING: This is for RESEARCH PURPOSES ONLY ⚠️
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("🚨 VULNERABLE LLM RESEARCH ENVIRONMENT SETUP 🚨")
    print("=" * 60)
    print("⚠️  WARNING: This setup is for RESEARCH PURPOSES ONLY ⚠️")
    print("🔓 Contains intentional security vulnerabilities")
    print("🚫 DO NOT use in production environments")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("✅ Python 3.8+ required")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True

def check_system_info():
    """Display system information"""
    print("\n💻 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Python: {sys.version}")
    
    # Check for CUDA
    try:
        import torch
        if torch.cuda.is_available():
            print(f"   CUDA: Available ({torch.cuda.get_device_name(0)})")
            print(f"   CUDA Version: {torch.version.cuda}")
        else:
            print("   CUDA: Not available (CPU-only mode)")
    except ImportError:
        print("   CUDA: PyTorch not installed yet")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    print("\n🔍 Checking installed dependencies...")
    
    required_packages = [
        "torch", "transformers", "auto_gptq", "fastapi", 
        "uvicorn", "accelerate", "sentencepiece", "pydantic"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        return False
    else:
        print("\n✅ All dependencies are installed")
        return True

def create_test_script():
    """Create a simple test script"""
    print("\n🧪 Creating test script...")
    
    test_script = """#!/usr/bin/env python3
\"\"\"
🧪 Simple test script for vulnerable LLM server
\"\"\"

import requests
import json

def test_server():
    \"\"\"Test basic server functionality\"\"\"
    try:
        # Test server info
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Server is running")
            data = response.json()
            print(f"📋 Model: {data.get('model', 'Unknown')}")
            print(f"🔓 Vulnerabilities: {len(data.get('vulnerabilities', []))}")
        else:
            print(f"❌ Server returned status: {response.status_code}")
            
        # Test secrets endpoint
        response = requests.get("http://localhost:8000/secrets")
        if response.status_code == 200:
            print("✅ Secrets endpoint accessible")
            secrets = response.json()
            print(f"🔑 Available secrets: {len(secrets.get('secrets', {}))}")
        else:
            print(f"❌ Secrets endpoint failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_server()
"""
    
    with open("test_server.py", "w") as f:
        f.write(test_script)
    
    print("✅ Test script created: test_server.py")

def create_startup_script():
    """Create startup script for easy server launch"""
    print("\n🚀 Creating startup script...")
    
    if platform.system() == "Windows":
        startup_script = """@echo off
echo 🚨 STARTING VULNERABLE LLM RESEARCH SERVER 🚨
echo ⚠️  WARNING: This server has intentional security vulnerabilities ⚠️
echo.
python vulnerable_llm_server.py
pause
"""
        script_name = "start_server.bat"
    else:
        startup_script = """#!/bin/bash
echo "🚨 STARTING VULNERABLE LLM RESEARCH SERVER 🚨"
echo "⚠️  WARNING: This server has intentional security vulnerabilities ⚠️"
echo ""
python3 vulnerable_llm_server.py
"""
        script_name = "start_server.sh"
        # Make executable
        os.chmod(script_name, 0o755)
    
    with open(script_name, "w") as f:
        f.write(startup_script)
    
    print(f"✅ Startup script created: {script_name}")

def display_usage_instructions():
    """Display usage instructions"""
    print("\n" + "=" * 60)
    print("🎯 SETUP COMPLETE - USAGE INSTRUCTIONS")
    print("=" * 60)
    
    print("\n1️⃣ Start the vulnerable server:")
    if platform.system() == "Windows":
        print("   start_server.bat")
    else:
        print("   ./start_server.sh")
    print("   OR")
    print("   python vulnerable_llm_server.py")
    
    print("\n2️⃣ Test the server:")
    print("   python test_server.py")
    
    print("\n3️⃣ Run attack examples:")
    print("   python attack_examples.py")
    
    print("\n4️⃣ Manual testing:")
    print("   curl http://localhost:8000/")
    print("   curl http://localhost:8000/secrets")
    
    print("\n📋 Available endpoints:")
    print("   - GET  / (server info)")
    print("   - GET  /secrets (exposed secrets)")
    print("   - GET  /debug (internal state)")
    print("   - POST /chat (vulnerable chat)")
    print("   - POST /swap_model (model swapping)")
    print("   - POST /execute (command injection)")
    
    print("\n⚠️  IMPORTANT WARNINGS:")
    print("   - NEVER expose to internet")
    print("   - NEVER use in production")
    print("   - NEVER use real secrets")
    print("   - ALWAYS use isolated environment")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Python 3.8+ required")
        sys.exit(1)
    
    # Display system info
    check_system_info()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed: Missing dependencies")
        sys.exit(1)
    
    # Create helper scripts
    create_test_script()
    create_startup_script()
    
    # Display usage instructions
    display_usage_instructions()
    
    print("\n🎉 Setup completed successfully!")
    print("🚨 Remember: This is for RESEARCH PURPOSES ONLY!")

if __name__ == "__main__":
    main()
