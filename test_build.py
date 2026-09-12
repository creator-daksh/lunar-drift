#!/usr/bin/env python3
"""Test and verify Lunar Drift can be imported and basic functions work"""
import sys
import os

def test_imports():
    """Test that all imports work"""
    print("[TEST] Checking Python imports...")
    try:
        import kivy
        print("  ✓ Kivy imported")
    except ImportError as e:
        print(f"  ✗ Kivy import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("  ✓ Pillow imported")
    except ImportError as e:
        print(f"  ✗ Pillow import failed: {e}")
        return False
    
    return True

def test_main_module():
    """Test main application module"""
    print("[TEST] Checking main.py syntax...")
    try:
        with open('main.py', 'r') as f:
            code = f.read()
        compile(code, 'main.py', 'exec')
        print("  ✓ main.py compiles successfully")
        return True
    except SyntaxError as e:
        print(f"  ✗ Syntax error in main.py: {e}")
        return False

def test_assets():
    """Test asset generation"""
    print("[TEST] Checking asset generation...")
    try:
        from create_assets import create_icons, create_presplash
        print("  ✓ Asset generators imported")
        return True
    except ImportError as e:
        print(f"  ✗ Asset generator import failed: {e}")
        return False

def test_buildozer_config():
    """Test buildozer configuration"""
    print("[TEST] Checking buildozer.spec...")
    if not os.path.exists('buildozer.spec'):
        print("  ✗ buildozer.spec not found")
        return False
    
    with open('buildozer.spec', 'r') as f:
        content = f.read()
    
    required_keys = ['[app]', 'title', 'package.name', 'requirements', 'android.api']
    for key in required_keys:
        if key not in content:
            print(f"  ✗ Missing '{key}' in buildozer.spec")
            return False
    
    print("  ✓ buildozer.spec configured correctly")
    return True

def main():
    print("="*50)
    print("Lunar Drift - Build Verification Tests")
    print("="*50)
    print()
    
    tests = [
        test_imports,
        test_main_module,
        test_assets,
        test_buildozer_config,
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    passed = sum(results)
    total = len(results)
    
    print("="*50)
    print(f"Results: {passed}/{total} tests passed")
    print("="*50)
    
    if all(results):
        print("\n✓ All tests passed! Ready to build APK")
        print("\nRun: buildozer android debug")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
