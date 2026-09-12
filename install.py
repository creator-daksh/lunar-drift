#!/usr/bin/env python3
"""Quick installer script for development"""
import subprocess
import os
import sys

def run(cmd, description=""):
    """Run command with status"""
    if description:
        print(f"[*] {description}")
    print(f"    Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"    FAILED!")
        return False
    return True

def main():
    print("=== Lunar Drift Quick Install ===")
    print()
    
    # Check for ADB
    if subprocess.run("adb --version", shell=True, capture_output=True).returncode != 0:
        print("ERROR: adb not found in PATH")
        print("Install Android SDK Platform Tools")
        return False
    
    # Find APK
    apk_files = [f for f in os.listdir('bin') if f.endswith('.apk')]
    if not apk_files:
        print("ERROR: No APK found in bin/")
        print("Build with: buildozer android debug")
        return False
    
    apk = os.path.join('bin', sorted(apk_files)[-1])  # Latest APK
    print(f"Found APK: {apk}")
    print()
    
    # Check device
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    if 'device' not in result.stdout:
        print("ERROR: No Android device found via ADB")
        print("Connect device via USB and enable USB debugging")
        return False
    
    print("Android device found")
    print()
    
    # Install
    if not run(f"adb install -r {apk}", "Installing APK"):
        return False
    
    print()
    print("Installation complete!")
    print()
    print("Next steps:")
    print("1. Open Lunar Drift app")
    print("2. Tap 'Set as Wallpaper'")
    print("3. Select 'Lunar Drift' from wallpaper picker")
    print("4. Tap Apply")
    print()
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
