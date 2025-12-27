"""
Quick setup script for Promptification
Helps verify installation and create necessary files
"""

import os
import sys
from pathlib import Path


def main():
    """Run setup checks and create necessary directories"""
    
    print("🎯 Promptification Setup")
    print("=" * 50)
    
    # Check Python version
    print("\n✓ Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"  Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check if in project directory
    print("\n✓ Checking project structure...")
    required_files = ['app.py', 'requirements.txt', 'README.md']
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Missing required file: {file}")
            print("   Make sure you're in the project root directory")
            return False
    print("  All required files present")
    
    # Check required directories
    print("\n✓ Checking directories...")
    required_dirs = ['models', 'personas', 'utils', 'app/pages', 'tests', 'data']
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            print(f"  Creating {dir_name}/")
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            print(f"  {dir_name}/ exists")
    
    # Check .env file
    print("\n✓ Checking environment configuration...")
    if not Path('.env').exists():
        if Path('.env.example').exists():
            print("  ⚠️  No .env file found")
            print("  Please copy .env.example to .env and add your API key:")
            print("     cp .env.example .env  (Linux/Mac)")
            print("     copy .env.example .env  (Windows)")
        else:
            print("  ❌ No .env.example file found")
            return False
    else:
        print("  .env file exists")
    
    # Check if dependencies are installed
    print("\n✓ Checking dependencies...")
    try:
        import streamlit
        print(f"  Streamlit {streamlit.__version__} installed")
    except ImportError:
        print("  ⚠️  Streamlit not installed")
        print("  Run: pip install -r requirements.txt")
        return False
    
    try:
        import pydantic
        print(f"  Pydantic {pydantic.__version__} installed")
    except ImportError:
        print("  ⚠️  Pydantic not installed")
        print("  Run: pip install -r requirements.txt")
        return False
    
    # Success message
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Make sure .env has your API key")
    print("2. Run the app: streamlit run app.py")
    print("3. Open browser at: http://localhost:8501")
    print("\nHappy prompting! 🎯")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
