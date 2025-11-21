"""
Quick Setup Script for EduQuest
Helps users configure their environment
"""
import os
import sys


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required = {
        'google.generativeai': 'google-generativeai',
        'dotenv': 'python-dotenv',
        'colorama': 'colorama'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"❌ {package} not found")
            missing.append(package)
    
    if missing:
        print(f"\nInstall missing packages with:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True


def check_env_file():
    """Check if .env file exists and has API key"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("\nCreate .env file:")
        print("1. Copy .env.example to .env")
        print("2. Get your API key from: https://makersuite.google.com/app/apikey")
        print("3. Add it to .env: GEMINI_API_KEY=your_key_here")
        return False
    
    print("✓ .env file exists")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("⚠ API key not configured in .env")
        print("  Get your key from: https://makersuite.google.com/app/apikey")
        return False
    
    print("✓ API key configured")
    return True


def main():
    """Run all checks"""
    print("=" * 60)
    print("EduQuest Setup Checker")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Config", check_env_file),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 40)
        results.append(check_func())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ All checks passed! You're ready to run EduQuest")
        print("\nStart EduQuest with:")
        print("  python eduquest.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
