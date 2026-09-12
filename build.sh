#!/bin/bash
# Quick build script for Lunar Drift APK

set -e

echo "=== Lunar Drift APK Builder ==="
echo ""

if ! command -v buildozer &> /dev/null; then
    echo "ERROR: buildozer not found"
    echo "Install with: pip install buildozer cython"
    exit 1
fi

echo "[1/4] Generating assets..."
python3 create_assets.py

echo "[2/4] Checking environment..."
if [ -z "$ANDROID_SDK_ROOT" ]; then
    echo "WARNING: ANDROID_SDK_ROOT not set"
fi

if [ -z "$ANDROID_NDK" ]; then
    echo "WARNING: ANDROID_NDK not set"
fi

echo "[3/4] Building APK (this may take 10-30 minutes)..."
buildozer android debug

echo "[4/4] Done!"
echo ""
echo "APK location: bin/lunardrift-*.apk"
echo ""
echo "To install:"
echo "  adb install -r bin/lunardrift-*.apk"
