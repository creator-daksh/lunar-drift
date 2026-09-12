"""
Lunar Drift Wallpaper Service
Android Live Wallpaper implementation using Kivy
"""

import os
os.environ['KIVY_WINDOW'] = 'pygame'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, PushMatrix, PopMatrix
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import numpy as np
from datetime import datetime
import json
from pathlib import Path
import threading
import time

try:
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
    PythonJavaClass = autoclass('org.kivy.android.PythonJavaClass')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    ANDROID_AVAILABLE = True
except ImportError:
    ANDROID_AVAILABLE = False
    PythonActivity = None


class MoonPhysics:
    """Handles moon physics, lighting, and animation."""
    
    def __init__(self):
        self.phase = 0.5
        self.illumination = 0.5
        self.rotation = 0
        self.latitude = 0
        self.longitude = 0
        self.time_elapsed = 0
        self.libration_x = 0
        self.libration_y = 0
        self.crater_detail = []
        
        self._generate_crater_map()
    
    def _generate_crater_map(self):
        """Generate realistic crater positions."""
        np.random.seed(42)  # Consistent crater pattern
        self.crater_detail = [
            {'name': 'Tycho', 'x': 0.3, 'y': -0.4, 'size': 0.08, 'depth': 0.7},
            {'name': 'Copernicus', 'x': -0.2, 'y': 0.3, 'size': 0.07, 'depth': 0.6},
            {'name': 'Aristarchus', 'x': -0.35, 'y': 0.25, 'size': 0.06, 'depth': 0.8},
            {'name': 'Clavius', 'x': -0.1, 'y': -0.35, 'size': 0.09, 'depth': 0.65},
            {'name': 'Theophilus', 'x': 0.25, 'y': 0.15, 'size': 0.05, 'depth': 0.7},
        ]
    
    def update(self, dt, device_x=0, device_y=0, is_stable=False):
        """Update moon physics."""
        self.time_elapsed += dt
        
        # Lunar phase cycle (29.5 days compressed to 30 seconds)
        self.phase = 0.5 + 0.5 * np.sin(self.time_elapsed * np.pi / 15)
        
        # Illumination based on phase
        self.illumination = 0.5 + 0.5 * np.cos(self.time_elapsed * np.pi / 15)
        
        # Gentle rotation
        self.rotation = (self.time_elapsed * 5) % 360
        
        # Libration (moon's subtle wobble)
        self.libration_x = 0.1 * np.sin(self.time_elapsed * 0.3)
        self.libration_y = 0.08 * np.cos(self.time_elapsed * 0.25)
        
        # Parallax from device motion
        if not is_stable:
            self.latitude = device_y * 30  # -30 to +30 degrees
            self.longitude = device_x * 45  # -45 to +45 degrees


class MoonRenderer(Widget):
    """Renders the moon with realistic shading and texturing."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.physics = MoonPhysics()
        self.parallax_offset_x = 0
        self.parallax_offset_y = 0
        self.glow_intensity = 1.0
        self.pulse_factor = 1.0
        self.is_stable = False
        self.last_motion_time = 0
        
        self.bind(size=self.on_size)
        Clock.schedule_interval(self.update_frame, 0.016)  # 60 FPS
    
    def on_size(self, *args):
        """Handle window resize."""
        self.canvas.clear()
    
    def update_frame(self, dt):
        """Update and render frame."""
        # Update physics
        self.physics.update(
            dt,
            device_x=self.parallax_offset_x / 100,
            device_y=self.parallax_offset_y / 100,
            is_stable=self.is_stable
        )
        
        self.canvas.clear()
        self.draw_background()
        self.draw_moon()
    
    def draw_background(self):
        """Draw space background."""
        from kivy.graphics import Color, Rectangle
        
        with self.canvas.before:
            # Deep space gradient (dark blue to black)
            Color(0.02, 0.03, 0.08, 1.0)
            Rectangle(size=self.size, pos=self.pos)
    
    def draw_moon(self):
        """Draw detailed moon sphere."""
        from kivy.graphics import Color, Ellipse, Line
        
        with self.canvas:
            # Calculate moon position with parallax
            center_x = self.center_x + self.parallax_offset_x
            center_y = self.center_y + self.parallax_offset_y
            moon_radius = min(self.width, self.height) * 0.2
            
            # Outer atmospheric glow
            glow_color = (1, 0.95, 0.85, 0.15 * self.glow_intensity)
            Color(*glow_color)
            Ellipse(
                pos=(center_x - moon_radius * 1.6, center_y - moon_radius * 1.6),
                size=(moon_radius * 3.2, moon_radius * 3.2)
            )
            
            # Middle glow layer
            Color(1, 0.9, 0.8, 0.3 * self.glow_intensity)
            Ellipse(
                pos=(center_x - moon_radius * 1.35, center_y - moon_radius * 1.35),
                size=(moon_radius * 2.7, moon_radius * 2.7)
            )
            
            # Inner bright glow
            Color(1, 0.98, 0.95, 0.5 * self.glow_intensity)
            Ellipse(
                pos=(center_x - moon_radius * 1.15, center_y - moon_radius * 1.15),
                size=(moon_radius * 2.3, moon_radius * 2.3)
            )
            
            # Main moon sphere
            Color(0.92, 0.92, 0.88, 1.0)
            Ellipse(
                pos=(center_x - moon_radius, center_y - moon_radius),
                size=(moon_radius * 2, moon_radius * 2)
            )
            
            # Draw phase shadow
            phase_ratio = abs(self.physics.phase - 0.5) * 2
            shadow_width = moon_radius * 2 * (1 - phase_ratio)
            shadow_offset = moon_radius * (self.physics.phase - 0.5) * 2
            
            Color(0.1, 0.1, 0.12, 0.8)
            Ellipse(
                pos=(center_x - moon_radius + shadow_offset, center_y - moon_radius),
                size=(shadow_width, moon_radius * 2)
            )
            
            # Draw terminator (day/night boundary) gradient
            if 0.25 < self.physics.phase < 0.75:
                terminator_x = center_x + moon_radius * (self.physics.phase - 0.5) * 2
                Color(0.15, 0.15, 0.18, 0.4)
                Ellipse(
                    pos=(terminator_x - 5, center_y - moon_radius),
                    size=(10, moon_radius * 2)
                )
            
            # Draw craters
            self._draw_craters(center_x, center_y, moon_radius)
            
            # Draw moon limb (edge highlight)
            Color(0.98, 0.97, 0.95, 0.3)
            Line(
                circle=(center_x, center_y, moon_radius),
                width=2
            )
    
    def _draw_craters(self, center_x, center_y, moon_radius):
        """Draw crater details on moon surface."""
        from kivy.graphics import Color, Ellipse, Line
        
        for crater in self.physics.crater_detail:
            # Crater position (affected by libration)
            crater_x = (crater['x'] + self.physics.libration_x) * moon_radius
            crater_y = (crater['y'] + self.physics.libration_y) * moon_radius
            crater_pos_x = center_x + crater_x
            crater_pos_y = center_y + crater_y
            
            crater_size = crater['size'] * moon_radius * 2
            
            # Crater shadow (depth)
            Color(0.6, 0.6, 0.58, 0.4)
            Ellipse(
                pos=(crater_pos_x - crater_size/2, crater_pos_y - crater_size/2),
                size=(crater_size, crater_size)
            )
            
            # Crater rim highlight
            Color(0.88, 0.88, 0.85, 0.5)
            Line(
                circle=(crater_pos_x, crater_pos_y, crater_size/2),
                width=1
            )
    
    def set_parallax(self, x, y):
        """Set parallax offset from device motion."""
        max_offset = min(self.width, self.height) * 0.08
        self.parallax_offset_x = np.clip(x, -max_offset, max_offset)
        self.parallax_offset_y = np.clip(y, -max_offset, max_offset)
    
    def set_stable(self, is_stable):
        """Set stability state."""
        self.is_stable = is_stable
        if is_stable:
            # Smoothly return parallax to center
            self.parallax_offset_x *= 0.95
            self.parallax_offset_y *= 0.95
    
    def pulse(self):
        """Trigger pulse animation."""
        self.pulse_factor = 1.15
        Clock.schedule_once(lambda dt: setattr(self, 'pulse_factor', 1.0), 0.4)


class SensorBridge:
    """Bridges device sensors (accelerometer, gyroscope) to the wallpaper."""
    
    def __init__(self, on_motion=None):
        self.on_motion = on_motion
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 9.8
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0
        
        self.is_stable = False
        self.stability_timer = 0
        self.motion_threshold = 0.8
        self.stability_threshold = 3.0
        
        self.sensor_thread = None
        self.running = False
        
        if ANDROID_AVAILABLE:
            self._init_android_sensors()
    
    def _init_android_sensors(self):
        """Initialize Android sensors."""
        try:
            request_permissions([Permission.BODY_SENSORS])
            # Sensor initialization handled via JNI bridge
        except Exception as e:
            print(f"Sensor init failed: {e}")
    
    def update(self, dt):
        """Update sensor state and stability detection."""
        # Calculate motion magnitude
        motion = np.sqrt(self.accel_x**2 + self.accel_y**2)
        
        # Stability detection
        if motion < self.motion_threshold:
            self.stability_timer += dt
            if self.stability_timer >= self.stability_threshold:
                self.is_stable = True
        else:
            self.is_stable = False
            self.stability_timer = 0
        
        # Callback
        if self.on_motion:
            self.on_motion(self.accel_x, self.accel_y, self.is_stable)
    
    def simulate_motion(self):
        """Simulate device motion for testing (when sensors unavailable)."""
        t = time.time()
        self.accel_x = 0.3 * np.sin(t * 0.5)
        self.accel_y = 0.2 * np.cos(t * 0.3)


class LunarDriftWallpaper(App):
    """Main Lunar Drift Wallpaper application."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Lunar Drift'
        self.icon = 'data/icon.png'
        self.moon_renderer = None
        self.sensor_bridge = None
        self.tap_detection = {'count': 0, 'time': 0, 'x': 0, 'y': 0}
        self.settings = self.load_settings()
    
    def build(self):
        """Build the wallpaper interface."""
        # Full screen
        Window.fullscreen = 'auto'
        
        # Root layout
        root = FloatLayout()
        
        # Moon renderer
        self.moon_renderer = MoonRenderer(size_hint=(1, 1))
        root.add_widget(self.moon_renderer)
        
        # Sensor bridge
        self.sensor_bridge = SensorBridge(on_motion=self.on_sensor_motion)
        Clock.schedule_interval(self.sensor_bridge.update, 0.016)
        Clock.schedule_interval(self.sensor_bridge.simulate_motion, 0.016)
        
        # Touch handler
        root.bind(on_touch_down=self.on_touch_down)
        
        # Apply saved settings
        self.apply_settings()
        
        return root
    
    def on_sensor_motion(self, accel_x, accel_y, is_stable):
        """Handle sensor motion events."""
        max_parallax = min(self.root.width, self.root.height) * 0.12
        
        self.moon_renderer.set_parallax(
            accel_x * max_parallax * 3,
            -accel_y * max_parallax * 3
        )
        
        self.moon_renderer.set_stable(is_stable)
    
    def on_touch_down(self, instance, touch):
        """Handle touch input for double-tap detection."""
        current_time = datetime.now().timestamp()
        
        # Double-tap detection (within 300ms)
        if current_time - self.tap_detection['time'] < 0.3:
            distance = np.sqrt(
                (touch.x - self.tap_detection['x'])**2 +
                (touch.y - self.tap_detection['y'])**2
            )
            if distance < 80:  # Within 80 pixels
                # Double tap detected - trigger pulse
                self.moon_renderer.pulse()
                self.tap_detection['count'] = 0
                return True
        
        self.tap_detection['time'] = current_time
        self.tap_detection['x'] = touch.x
        self.tap_detection['y'] = touch.y
        self.tap_detection['count'] += 1
        
        return True
    
    def apply_settings(self):
        """Apply loaded settings."""
        if self.moon_renderer:
            self.moon_renderer.glow_intensity = self.settings.get('glow_intensity', 1.0)
    
    def load_settings(self):
        """Load settings from persistent storage."""
        try:
            settings_file = Path.home() / '.lunar_drift_settings.json'
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Settings load error: {e}")
        return {'glow_intensity': 1.0}
    
    def save_settings(self):
        """Save settings to persistent storage."""
        try:
            settings_file = Path.home() / '.lunar_drift_settings.json'
            with open(settings_file, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Settings save error: {e}")


if __name__ == '__main__':
    app = LunarDriftWallpaper()
    app.run()
