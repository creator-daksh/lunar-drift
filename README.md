# Lunar Drift - Android Live Wallpaper

## Overview

Lunar Drift is a beautiful animated moon wallpaper for Android with gyroscope parallax, swipe control, and motion-aware power saving.

### Features
- ✨ Animated moon with glowing, pulsing effect
- ✨ Gyroscope parallax - moon follows device tilt
- ✨ Swipe left/right manual control
- ✨ Double-tap pulse animation
- ✨ Motion stability detection (3-second pause)
- ✨ Sensor filtering & smoothing
- ✨ Starfield background
- ✨ Completely offline
- ✨ Minimal permissions (BODY_SENSORS only)
- ✨ Android 5.0+ support

## Quick Start

### For Users
1. Download `Lunar Drift.apk`
2. Open on Android device
3. Tap "Set as Wallpaper"
4. Select "Lunar Drift"
5. Choose "Home screen"

### For Developers
```bash
git clone https://github.com/creator-daksh/lunar-drift.git
cd lunar-drift
pip install buildozer cython kivy
buildozer android debug
adb install bin/lunardrift-*.apk
```

## Controls
- **Tilt Device**: Move moon with gyroscope
- **Swipe Left/Right**: Manual parallax
- **Double-Tap**: Pulse animation
- **Auto-Pause**: After 3 seconds of stillness

## Technology
- Python 3 + Kivy 2.2.1
- Android NDK/SDK
- Buildozer APK generation
- 60 FPS rendering

## Permissions
- BODY_SENSORS: Gyroscope/accelerometer
- No internet, camera, or location needed

## Documentation
- [Installation Guide](INSTALL.md)
- [Build Instructions](BUILD.md)
- [Changelog](CHANGELOG.md)

## License
MIT - Open source and free to modify

## Links
- GitHub: https://github.com/creator-daksh/lunar-drift
