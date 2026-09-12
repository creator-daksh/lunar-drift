# Lunar Drift - Version 1.0.0 Release Notes

## Release Date: September 12, 2026

### Overview
Lunar Drift v1.0.0 is the initial release of a production-ready Android live wallpaper featuring an animated moon with gyroscope parallax control, swipe gestures, double-tap effects, and motion-aware power optimization.

### System Requirements
- **Android Version:** 5.0 or later (API level 21+)
- **RAM:** 50+ MB available
- **Storage:** 50-80 MB for APK
- **Sensors:** Gyroscope recommended (accelerometer as fallback)
- **Display:** Any Android tablet or phone

### What's New in 1.0.0

#### Core Features
- **Moon Animation**
  - Glowing, pulsing moon rendering
  - Realistic crater shadows
  - 60 FPS smooth animation
  - Customizable glow intensity

- **Gyroscope Parallax**
  - Real-time device tilt tracking
  - Smooth sensor filtering (rolling averages)
  - Accelerometer integration for stability
  - Configurable parallax strength

- **Touch Controls**
  - Swipe left/right for manual parallax
  - Smooth deceleration physics
  - Double-tap pulse animation
  - Bounds checking to keep moon visible

- **Power Optimization**
  - 3-second motion stability detection
  - Auto-pause animation when idle
  - Instant resume on motion detected
  - Significant battery savings

- **Live Wallpaper**
  - Full Android wallpaper service integration
  - Appears in system wallpaper picker
  - Selectable for home and lock screens
  - Runs in background seamlessly

#### Technical Features
- 60 FPS hardware-accelerated rendering
- Gyroscope + Accelerometer support
- Sensor data smoothing (5/10 sample averages)
- Starfield background with 100+ stars
- Motion magnitude calculations
- Touch event detection and tracking

#### User Experience
- Intuitive tilt-to-move control
- Visual feedback (glow, pulse effects)
- No configuration required (works out-of-box)
- Graceful handling of missing sensors
- Smooth, fluid animations

#### Security & Privacy
- Minimal permissions (BODY_SENSORS only)
- No internet access required
- No data collection
- Complete offline operation
- Local settings storage only

### File Structure
```
lunar-drift/
├── main.py                      # Core application
├── wallpaper_service.py         # Android service
├── buildozer.spec               # Build config
├── android/                     # Android resources
├── data/                        # Assets (icons)
└── [documentation]              # Guides & README
```

### Build Information
- **Build System:** Buildozer + python-for-android
- **Python Version:** 3.8+
- **Kivy Version:** 2.2.1
- **Android NDK:** 25b
- **Android SDK:** API 21-33

### Known Limitations
1. Sensors only available on physical Android devices
2. Some Android emulators don't support motion sensors
3. Desktop version (without Android) uses simulated sensors
4. Wallpaper rendering performance varies by device hardware
5. Settings are stored locally (no cloud sync in v1.0)

### Permissions Granted
- `android.permission.BODY_SENSORS` - Gyroscope/accelerometer
- `android.permission.VIBRATE` - Optional future use
- `android.permission.WAKE_LOCK` - Wallpaper rendering
- `android.permission.CHANGE_CONFIGURATION` - Orientation

### Performance Metrics
- **Frame Rate:** 60 FPS target
- **Memory Usage:** ~50-100 MB
- **APK Size:** ~50-80 MB
- **Battery Impact:** Minimal (with auto-pause)
- **Sensor Update Rate:** ~60 Hz

### Installation Instructions

#### Quick Install (Users)
1. Download `Lunar Drift.apk`
2. Open file on Android device
3. Tap Install
4. Open app and tap "Set as Wallpaper"
5. Select from wallpaper picker

#### Developer Build
```bash
git clone https://github.com/creator-daksh/lunar-drift.git
cd lunar-drift
pip install buildozer cython kivy==2.2.1
python3 create_assets.py
buildozer android debug
adb install -r bin/lunardrift-1.0.0-debug.apk
```

### Testing Performed

✅ **Code Quality**
- Python syntax validation
- Import dependency checking
- Configuration verification

✅ **Functionality**
- Moon rendering verified
- Animation smoothness at 60 FPS
- Gyroscope input detection
- Swipe gesture recognition
- Double-tap detection
- Motion stability detection
- Sensor filtering applied

✅ **Integration**
- Android manifest validation
- Wallpaper service registration
- Live wallpaper service working
- Permission handling
- Orientation support

✅ **Build Verification**
- APK generation successful
- Package contents validated
- Resource compilation verified
- No missing dependencies

### Known Issues (None in v1.0.0)
- All identified issues resolved
- Ready for production use

### Future Roadmap

#### v1.1.0 (Planned)
- Customizable settings screen
- Multiple moon phases
- Adjustable animation speed
- User-configurable color schemes

#### v1.2.0 (Planned)
- Haptic feedback (vibration)
- Performance metrics display
- Cloud preferences sync
- Additional wallpaper themes

#### v2.0.0 (Planned)
- Advanced animations
- Multiple wallpaper modes
- Community themes
- Desktop version (Windows/macOS)

### Support & Feedback

**GitHub Repository**
- https://github.com/creator-daksh/lunar-drift
- Issue tracking
- Pull request support

**Documentation**
- README.md - Overview
- INSTALL.md - Installation guide
- BUILD.md - Build instructions
- STRUCTURE.md - Project layout
- CHANGELOG.md - Version history

### Credits

**Technology Stack**
- Kivy: UI framework and graphics
- Python: Core language
- Buildozer: APK generation
- Android SDK/NDK: Native integration

**Inspired by**
- Android live wallpaper APIs
- Motion sensor programming
- Real-time graphics rendering

### License

MIT License - Open source and free to use

```
Copyright (c) 2026 Lunar Drift Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

### Version Information

- **App Version:** 1.0.0
- **Build Number:** 1
- **Release Date:** September 12, 2026
- **API Level:** 21-33
- **Python Version:** 3.8+
- **Kivy Version:** 2.2.1

---

**Thank you for using Lunar Drift!**

Enjoy the moon. 🌙
