# Lunar Drift Project Structure

```
lunar-drift/
├── main.py                    # Core Kivy application
├── wallpaper_service.py       # Android service bridge
├── create_assets.py           # Asset/icon generator
├── generate_icons.py          # Icon generation utility
├── build.sh                   # Build automation script
├── install.py                 # Installation helper
│
├── buildozer.spec             # Buildozer configuration
├── README.md                  # Project overview
├── INSTALL.md                 # Installation guide
├── BUILD.md                   # Build instructions
├── CHANGELOG.md               # Version history
│
├── android/
│   ├── AndroidManifest.xml    # Android manifest
│   └── res/
│       ├── xml/
│       │   └── wallpaper.xml  # Wallpaper metadata
│       └── values/
│           └── strings.xml    # String resources
│
├── data/
│   ├── icon.png               # App icon (generated)
│   └── presplash.png          # Splash screen (generated)
│
├── recipes/
│   └── __init__.py            # Custom recipe directory
│
└── .github/
    └── workflows/
        └── build-apk.yml      # CI/CD automation
```

## File Descriptions

### Core Application
- **main.py**: Main Kivy application with UI, moon rendering, and sensor handling
- **wallpaper_service.py**: Android live wallpaper service bridge using PyJNI

### Build & Configuration
- **buildozer.spec**: Buildozer configuration for APK generation
- **build.sh**: Quick build script (Linux/macOS)
- **install.py**: ADB installation helper
- **create_assets.py**: Generates icon and presplash images

### Documentation
- **README.md**: Project overview and quick start
- **INSTALL.md**: End-user and developer installation guide
- **BUILD.md**: Detailed build instructions and troubleshooting
- **CHANGELOG.md**: Version history and feature list

### Android Resources
- **android/AndroidManifest.xml**: Android app manifest with permissions
- **android/res/xml/wallpaper.xml**: Live wallpaper metadata
- **android/res/values/strings.xml**: Localized string resources

### Assets
- **data/icon.png**: App icon (192x192px)
- **data/presplash.png**: Splash screen (1280x1280px)

### CI/CD
- **.github/workflows/build-apk.yml**: GitHub Actions workflow for automated builds

## Key Features Implemented

✓ Moon animation with glowing pulsing effect
✓ Gyroscope parallax control (device tilt)
✓ Swipe left/right manual control
✓ Double-tap pulse animation
✓ Motion stability detection (3-second threshold)
✓ Sensor filtering and smoothing
✓ Starfield background
✓ Live wallpaper service registration
✓ Minimal permissions (BODY_SENSORS only)
✓ Offline operation (no internet required)
✓ Android 5.0+ (API 21+) support
✓ Portrait and landscape orientation
✓ 60 FPS smooth rendering

## Build & Install Quick Reference

```bash
# Generate assets
python3 create_assets.py

# Build APK
buildozer android debug

# Install on device
adb install -r bin/lunardrift-*.apk

# Or use helper scripts
bash build.sh              # Linux/macOS
python3 install.py        # Install with ADB
```

## Technology Stack

- **Python 3.8+**: Core application logic
- **Kivy 2.2.1**: UI framework and graphics
- **Android NDK 25b**: Native code compilation
- **Buildozer**: APK generation and packaging
- **PyJNI**: Java/Python bridge for sensors
- **Pillow**: Image processing (icon generation)

## Permissions & Privacy

Required:
- `BODY_SENSORS`: Access gyroscope and accelerometer
- `WAKE_LOCK`: Live wallpaper rendering
- `CHANGE_CONFIGURATION`: Orientation handling

Optional:
- `VIBRATE`: Potential future haptic feedback

NOT required:
- Internet / Network access
- Camera / Microphone
- Location / GPS
- Storage access
- Contacts / SMS
- Accessibility services

## License

MIT License - Free to modify, distribute, and use commercially
