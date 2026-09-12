[app]
title = Lunar Drift
package.name = lunardrift
package.domain = org.lunardrift
version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

requirements = python3,kivy==2.2.1,pillow,jnius

orientation = sensorPortrait,sensorLandscape
fullscreen = 1

android.permissions = BODY_SENSORS,VIBRATE,WAKE_LOCK,CHANGE_CONFIGURATION
android.features = android.hardware.sensor.accelerometer,android.hardware.sensor.gyroscope

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

android.logcat_filters = *:S python:D

# Icon and presplash
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png

# Build configuration
log_level = 2
warn_on_root = 1

# Buildozer settings
p4a.bootstrap = sdl2
p4a.local_recipes = ./recipes
