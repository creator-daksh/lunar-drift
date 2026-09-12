# Build Instructions

## System Requirements
- Python 3.8+
- JDK 11+
- Android SDK (API 21+)
- Android NDK 25b
- Apache Ant
- 5-10 GB disk space

## Setup

### 1. Install Dependencies
```bash
# Ubuntu/Debian
sudo apt-get install -y build-essential libffi-dev python3-dev default-jdk git

# macOS
brew install python@3.11 openjdk@11 ant
```

### 2. Install Python Tools
```bash
pip install buildozer cython kivy==2.2.1
```

### 3. Setup Android SDK/NDK

**Using Android Studio:**
1. Download Android Studio
2. Open SDK Manager
3. Install Android SDK 33, Build-tools 33.0.0, NDK 25.1.8937393

**Or via command line:**
```bash
mkdir -p ~/Android/Sdk
wget https://dl.google.com/android/repository/commandlinetools-linux-latest.zip
unzip commandlinetools-linux-latest.zip
./cmdline-tools/bin/sdkmanager --sdk_root=~/Android/Sdk \
  "platform-tools" "platforms;android-33" "build-tools;33.0.0" "ndk;25.1.8937393"
```

### 4. Configure Environment
```bash
# Add to ~/.bashrc
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
export ANDROID_NDK=$HOME/Android/Sdk/ndk/25.1.8937393
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$ANDROID_SDK_ROOT/platform-tools:$PATH

source ~/.bashrc
```

### 5. Build
```bash
git clone https://github.com/creator-daksh/lunar-drift.git
cd lunar-drift
buildozer android debug
```

### 6. Install
```bash
adb install -r bin/lunardrift-1.0.0-debug.apk
```

## Troubleshooting

**Java not found:** Install JDK 11, set JAVA_HOME

**Android SDK not found:** Set ANDROID_SDK_ROOT, verify platforms exist

**NDK not found:** Download NDK 25b via sdkmanager

**Out of memory:** `export _JAVA_OPTIONS="-Xmx4096m"`

**Clean rebuild:** `rm -rf .buildozer build && buildozer android debug`

See detailed BUILD.md in repo for more info.
