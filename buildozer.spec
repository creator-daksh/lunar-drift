[app]
title = Lunar Drift
package.name = lunardrift
package.domain = com.lunardrift

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0.0

requirements = python3,kivy,numpy,jnius

orientation = sensor
fullscreen = 1
android.permissions = BODY_SENSORS
android.features = android.hardware.sensor.accelerometer,android.hardware.sensor.gyroscope

android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

android.logcat_filters = *:S python:D

# Wallpaper service
android.entrypoint = org.kivy.android.PythonService
android.services = LunarDriftWallpaper:LunarDriftWallpaper

# Android manifest additions
android.manifest_additions = 
	<uses-permission android:name="android.permission.BODY_SENSORS" />
	<service android:name=".LunarDriftWallpaper"
	    android:permission="android.permission.BIND_WALLPAPER">
	    <intent-filter>
	        <action android:name="android.service.wallpaper.WallpaperService" />
	    </intent-filter>
	    <meta-data android:name="android.service.wallpaper"
	        android:resource="@xml/wallpaper" />
	</service>

# Icon and presplash
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png

# Build configuration
log_level = 2
warn_on_root = 1
