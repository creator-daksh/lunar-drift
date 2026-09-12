#!/usr/bin/env python3
"""
Lunar Drift - Android Live Wallpaper
Moon animation with gyroscope parallax, swipe control, and sensor stability detection.
Built with Python and Kivy for cross-platform Android compatibility.
"""

import os
import math
import json
from datetime import datetime
from collections import deque

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

# Try to import Android-specific modules
try:
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    ANDROID_AVAILABLE = True
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
except (ImportError, RuntimeError):
    ANDROID_AVAILABLE = False
    print("[INFO] Android modules not available - running in desktop mode")


class SensorManager:
    """Manages Android sensor input (gyroscope, accelerometer)."""
    
    def __init__(self):
        self.gyro_x = 0.0
        self.gyro_y = 0.0
        self.gyro_z = 0.0
        self.accel_x = 0.0
        self.accel_y = 0.0
        self.accel_z = 0.0
        self.available = False
        
        if ANDROID_AVAILABLE:
            self._init_sensors()
    
    def _init_sensors(self):
        """Initialize Android sensors through JNI."""
        try:
            # Get system sensor manager
            activity = PythonActivity.mActivity
            Context = autoclass('android.content.Context')
            context = activity.getSystemService(Context.SENSOR_SERVICE)
            self.sensor_manager = context
            self.available = True
            print("[INFO] Android sensors initialized successfully")
        except Exception as e:
            print(f"[WARNING] Failed to initialize sensors: {e}")
            self.available = False
    
    def get_motion_magnitude(self):
        """Calculate total motion from all sensors."""
        return math.sqrt(
            self.gyro_x**2 + self.gyro_y**2 + self.gyro_z**2 +
            self.accel_x**2 + self.accel_y**2 + self.accel_z**2
        )


class LunarDriftWallpaper(Widget):
    """Main wallpaper widget with moon rendering and animations."""
    
    pulse = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.pos_hint = {'x': 0, 'y': 0}
        
        # Moon properties
        self.moon_x = 0.5
        self.moon_y = 0.5
        self.moon_scale = 0.15
        self.moon_radius = 100
        
        # Sensor management
        self.sensor_manager = SensorManager()
        
        # Motion detection and stability
        self.motion_detected = True
        self.stability_timer = 0.0
        self.stability_threshold = 3.0  # 3 seconds
        self.motion_threshold = 0.1
        self.motion_magnitude = 0.0
        
        # Animation states
        self.pulse_phase = 0.0
        self.pulse_speed = 2.0
        self.animation_enabled = True
        self.double_tap_detected = False
        self.double_tap_timer = 0.0
        self.last_tap_time = 0.0
        self.tap_count = 0
        
        # Swipe/parallax control
        self.swipe_offset = 0.0
        self.swipe_velocity = 0.0
        self.touch_start_x = 0.0
        self.touch_start_time = 0.0
        
        # Settings
        self.settings = {
            'animation_speed': 1.0,
            'parallax_strength': 1.0,
            'glow_intensity': 0.3,
            'show_stars': True,
        }
        
        # Event tracking
        self.bind(size=self.on_size)
        
        # Start animation loop
        Clock.schedule_interval(self.update, 1.0 / 60.0)  # 60 FPS
    
    def on_size(self, instance, value):
        """Handle window resize."""
        self.moon_radius = min(self.width, self.height) * self.moon_scale
        self.redraw_canvas()
    
    def on_touch_down(self, touch):
        """Handle touch down - detect double-tap and swipe start."""
        current_time = Clock.get_time()
        
        # Double-tap detection
        if current_time - self.last_tap_time < 0.3:
            self.tap_count += 1
            if self.tap_count >= 2:
                self.double_tap_detected = True
                self.double_tap_timer = 0.5
                self.tap_count = 0
        else:
            self.tap_count = 1
            self.last_tap_time = current_time
        
        # Track swipe
        self.touch_start_x = touch.x
        self.touch_start_time = current_time
        
        return True
    
    def on_touch_move(self, touch):
        """Handle touch move - update swipe offset."""
        delta_x = touch.x - self.touch_start_x
        self.swipe_offset = delta_x / max(self.width, 1) * 0.5
        self.swipe_offset = max(-0.25, min(0.25, self.swipe_offset))
        return True
    
    def on_touch_up(self, touch):
        """Handle touch up - calculate swipe velocity."""
        current_time = Clock.get_time()
        delta_time = current_time - self.touch_start_time
        
        if delta_time > 0:
            self.swipe_velocity = (touch.x - self.touch_start_x) / (delta_time * max(self.width, 1))
        
        return True
    
    def update(self, dt):
        """Update animation, sensors, and physics each frame."""
        # Update animation phases
        self.pulse_phase += dt * self.pulse_speed * self.settings['animation_speed']
        if self.pulse_phase >= 2 * math.pi:
            self.pulse_phase -= 2 * math.pi
        
        # Update pulse glow
        base_pulse = 1.0 + self.settings['glow_intensity'] * math.sin(self.pulse_phase)
        self.pulse = base_pulse if self.animation_enabled else 1.0
        
        # Update double-tap animation
        if self.double_tap_detected:
            self.double_tap_timer -= dt
            if self.double_tap_timer <= 0:
                self.double_tap_detected = False
        
        # Update motion detection
        self.motion_magnitude = self.sensor_manager.get_motion_magnitude()
        self.motion_detected = self.motion_magnitude > self.motion_threshold
        
        # Update stability timer
        if self.motion_detected:
            self.stability_timer = 0.0
        else:
            self.stability_timer += dt
        
        # Disable animation if stable for 3 seconds (save power)
        self.animation_enabled = self.stability_timer < self.stability_threshold
        
        # Decay swipe
        self.swipe_offset += self.swipe_velocity * dt
        self.swipe_velocity *= 0.95
        
        if abs(self.swipe_offset) < 0.001:
            self.swipe_offset = 0.0
            self.swipe_velocity = 0.0
        
        # Update moon position based on sensors and swipe
        parallax_strength = self.settings['parallax_strength']
        self.moon_x = 0.5 + (self.sensor_manager.gyro_y * 0.1 * parallax_strength) + self.swipe_offset
        self.moon_y = 0.5 - (self.sensor_manager.gyro_x * 0.1 * parallax_strength)
        
        # Clamp moon position
        self.moon_x = max(0.1, min(0.9, self.moon_x))
        self.moon_y = max(0.1, min(0.9, self.moon_y))
        
        # Redraw
        self.redraw_canvas()
    
    def redraw_canvas(self):
        """Render moon and background to canvas."""
        self.canvas.clear()
        
        with self.canvas:
            # Black space background
            Color(0.02, 0.02, 0.05, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # Starfield
            if self.settings['show_stars']:
                self._draw_stars()
            
            # Calculate moon position
            moon_center_x = self.x + self.moon_x * self.width
            moon_center_y = self.y + self.moon_y * self.height
            moon_radius = self.moon_radius
            
            # Moon glow (if animated)
            if self.animation_enabled:
                glow_radius = moon_radius * self.pulse
                Color(1, 1, 0.8, 0.15 * (1.5 - self.pulse) * self.settings['glow_intensity'])
                Ellipse(
                    pos=(moon_center_x - glow_radius, moon_center_y - glow_radius),
                    size=(glow_radius * 2, glow_radius * 2)
                )
            
            # Moon body
            Color(0.95, 0.95, 0.85, 1)
            Ellipse(
                pos=(moon_center_x - moon_radius, moon_center_y - moon_radius),
                size=(moon_radius * 2, moon_radius * 2)
            )
            
            # Moon craters
            Color(0.7, 0.7, 0.6, 1)
            crater_positions = [
                (0.3, 0.3, 0.15),
                (0.6, 0.5, 0.1),
                (0.4, 0.7, 0.12),
                (0.2, 0.6, 0.08),
            ]
            for cx, cy, cr in crater_positions:
                crater_x = moon_center_x - moon_radius + cx * moon_radius * 2
                crater_y = moon_center_y - moon_radius + cy * moon_radius * 2
                crater_r = cr * moon_radius
                Ellipse(
                    pos=(crater_x - crater_r, crater_y - crater_r),
                    size=(crater_r * 2, crater_r * 2)
                )
            
            # Double-tap pulse effect
            if self.double_tap_detected:
                pulse_size = 1.0 - (self.double_tap_timer / 0.5)
                pulse_radius = moon_radius * (1.5 + pulse_size * 0.5)
                Color(1, 0.8, 0.2, 0.5 * (1 - pulse_size))
                Ellipse(
                    pos=(moon_center_x - pulse_radius, moon_center_y - pulse_radius),
                    size=(pulse_radius * 2, pulse_radius * 2)
                )
    
    def _draw_stars(self):
        """Draw starfield background."""
        Color(1, 1, 1, 0.4)
        star_seed = 42
        for i in range(100):
            star_x = (self.x + (i * 97 + star_seed) % int(self.width))
            star_y = (self.y + (i * 71 + star_seed) % int(self.height))
            size = 1 + (i % 3)
            Ellipse(pos=(star_x, star_y), size=(size, size))


class LunarDriftApp(App):
    """Main application class for Lunar Drift."""
    
    def build(self):
        """Build the app UI."""
        Window.size = (720, 1280)
        Window.bind(on_keyboard=self.on_keyboard)
        
        # Request Android permissions
        if ANDROID_AVAILABLE:
            self._request_permissions()
        
        # Create root layout
        self.root = FloatLayout()
        
        # Add wallpaper widget
        self.wallpaper = LunarDriftWallpaper()
        self.root.add_widget(self.wallpaper)
        
        # Add UI overlay (settings button)
        self._add_ui_overlay()
        
        return self.root
    
    def _add_ui_overlay(self):
        """Add settings button to wallpaper."""
        overlay = FloatLayout(size_hint=(1, 1))
        
        # Settings button
        btn = Button(
            text='Set as Wallpaper',
            size_hint=(0.3, 0.08),
            pos_hint={'right': 1, 'top': 1}
        )
        btn.bind(on_press=self.on_set_wallpaper)
        overlay.add_widget(btn)
        
        self.root.add_widget(overlay)
    
    def on_set_wallpaper(self, instance):
        """Handle set wallpaper button press."""
        if ANDROID_AVAILABLE:
            try:
                Intent = autoclass('android.content.Intent')
                Settings = autoclass('android.provider.Settings')
                
                intent = Intent()
                intent.setAction(Settings.ACTION_DISPLAY_SETTINGS)
                
                activity = PythonActivity.mActivity
                activity.startActivity(intent)
            except Exception as e:
                print(f"[ERROR] Failed to open wallpaper settings: {e}")
        else:
            print("[INFO] Running in desktop mode - wallpaper setting not available")
    
    def _request_permissions(self):
        """Request necessary Android permissions."""
        try:
            permissions = [
                Permission.BODY_SENSORS,
            ]
            request_permissions(permissions)
        except Exception as e:
            print(f"[WARNING] Failed to request permissions: {e}")
    
    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle keyboard input."""
        if key == 27:  # ESC
            return True
        return False


if __name__ == '__main__':
    app = LunarDriftApp()
    app.run()
