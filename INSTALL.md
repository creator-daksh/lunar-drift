# Installation Guide

## For End Users

### Download & Install
1. Download `Lunar Drift.apk` from GitHub Releases
2. Open on Android device
3. Allow installation from unknown sources
4. Tap Install
5. Open Lunar Drift app
6. Tap "Set as Wallpaper"
7. Select "Lunar Drift" from wallpaper picker
8. Choose "Home screen"
9. Tap Apply

## For Developers

### Requirements
- Python 3.8+, Buildozer, Android SDK/NDK 25b, JDK 11+

### Build
```bash
git clone https://github.com/creator-daksh/lunar-drift.git
cd lunar-drift
pip install buildozer cython kivy==2.2.1
buildozer android debug
```

### Install
```bash
adb install -r bin/lunardrift-1.0.0-debug.apk
```

## Troubleshooting

**Wallpaper doesn't appear**
- Uninstall & reinstall
- Restart device
- Verify BODY_SENSORS permission

**Gyroscope not working**
- Check device has gyroscope
- Restart device

**Performance issues**
- Close other apps
- Restart device

See BUILD.md for detailed build instructions.
