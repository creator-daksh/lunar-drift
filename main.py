"""
Lunar Drift - Android Live Wallpaper
A beautiful, animated Moon wallpaper with gyroscope parallax control.
"""

import os
import sys
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.garden.matplotlib import pyplot as plt
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.gridlayout import GridLayout

import numpy as np
from datetime import datetime
import json
from pathlib import Path

# Android-specific imports
try:
    from jnius import autoclass
    from jnius import cast
    from android.permissions import request_permissions, Permission, check_permission
    from android.runnable import run_on_ui_thread
    from android import api_version
    ANDROID_AVAILABLE = True
except ImportError:
    ANDROID_AVAILABLE = False

try:
    from android.sensor import AndroidSensor
    SENSOR_AVAILABLE = True
except ImportError:
    SENSOR_AVAILABLE = False


class MoonRenderer(Widget):
    """Renders the moon with realistic shading and animation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.phase = 0.5
        self.rotation = 0
        self.glow_intensity = 1.0
        self.pulse_factor = 1.0
        self.parallax_x = 0
        self.parallax_y = 0
        self.time_elapsed = 0
        
        self.bind(size=self.update_canvas)
        Clock.schedule_interval(self.update, 0.016)  # ~60 FPS
        
    def update_canvas(self, *args):
        self.canvas.clear()
        self.draw_moon()
        
    def draw_moon(self):
        """Draw the moon using OpenGL rendering."""
        from kivy.graphics import Color, Ellipse, PushMatrix, PopMatrix, Translate, Rotate
        
        with self.canvas:
            PushMatrix()
            
            # Position with parallax
            moon_x = self.center_x + self.parallax_x
            moon_y = self.center_y + self.parallax_y
            moon_radius = min(self.width, self.height) * 0.25 * self.pulse_factor
            
            # Draw outer glow
            Color(1, 0.9, 0.8, 0.3 * self.glow_intensity)
            Ellipse(
                pos=(moon_x - moon_radius * 1.4, moon_y - moon_radius * 1.4),
                size=(moon_radius * 2.8, moon_radius * 2.8)
            )
            
            # Draw inner glow
            Color(1, 0.95, 0.9, 0.6 * self.glow_intensity)
            Ellipse(
                pos=(moon_x - moon_radius * 1.2, moon_y - moon_radius * 1.2),
                size=(moon_radius * 2.4, moon_radius * 2.4)
            )
            
            # Draw main moon sphere
            Color(0.95, 0.95, 0.9, 1.0)
            Ellipse(
                pos=(moon_x - moon_radius, moon_y - moon_radius),
                size=(moon_radius * 2, moon_radius * 2)
            )
            
            # Draw moon phase shadow
            phase_shadow_width = moon_radius * 2 * (1 - abs(self.phase - 0.5) * 2)
            shadow_offset = moon_radius * (self.phase - 0.5) * 2
            
            Color(0.1, 0.1, 0.15, 0.7)
            Ellipse(
                pos=(moon_x - moon_radius + shadow_offset, moon_y - moon_radius),
                size=(phase_shadow_width, moon_radius * 2)
            )
            
            # Draw craters for detail
            crater_positions = [
                (0.3, 0.3, 0.08),
                (-0.4, 0.2, 0.06),
                (0.1, -0.4, 0.07),
                (-0.2, -0.3, 0.05),
            ]
            
            Color(0.85, 0.85, 0.8, 0.5)
            for cx, cy, crater_r in crater_positions:
                crater_x = moon_x + cx * moon_radius
                crater_y = moon_y + cy * moon_radius
                crater_size = crater_r * moon_radius * 2
                Ellipse(
                    pos=(crater_x - crater_size/2, crater_y - crater_size/2),
                    size=(crater_size, crater_size)
                )
            
            PopMatrix()
    
    def update(self, dt):
        """Update animation state."""
        self.time_elapsed += dt
        
        # Moon phase cycles every 30 seconds
        self.phase = 0.5 + 0.5 * np.sin(self.time_elapsed * np.pi / 15)
        
        # Gentle rotation
        self.rotation = (self.time_elapsed * 5) % 360
        
        # Glow pulse
        self.glow_intensity = 0.7 + 0.3 * np.sin(self.time_elapsed * np.pi / 3)
        
        # Pulse effect (grows and shrinks)
        self.pulse_factor = 0.95 + 0.05 * np.sin(self.time_elapsed * np.pi / 2)
        
        self.canvas.ask_update()


class SensorManager:
    """Manages device sensors (accelerometer, gyroscope)."""
    
    def __init__(self, on_motion_callback=None):
        self.on_motion = on_motion_callback
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 9.8
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0
        self.is_stable = False
        self.stability_timer = 0
        self.motion_active = False
        self.motion_cooldown = 0
        
        self.sensors_available = False
        self._init_sensors()
        
    def _init_sensors(self):
        """Initialize device sensors if available."""
        if not ANDROID_AVAILABLE:
            return
            
        try:
            # Request sensor permissions if needed
            if ANDROID_AVAILABLE:
                request_permissions([Permission.BODY_SENSORS])
            self.sensors_available = True
        except Exception as e:
            print(f"Sensor initialization error: {e}")
            self.sensors_available = False
    
    def update(self, dt):
        """Update sensor readings and stability detection."""
        if not self.sensors_available:
            # Simulate gentle motion when sensors unavailable
            self.accel_x = np.random.normal(0, 0.1)
            self.accel_y = np.random.normal(0, 0.1)
            return
        
        # Read actual sensor data if available
        try:
            # This would be connected to actual device sensors via JNI
            pass
        except Exception as e:
            print(f"Sensor read error: {e}")
        
        # Detect stability (3 second threshold)
        motion_magnitude = np.sqrt(self.accel_x**2 + self.accel_y**2)
        
        if motion_magnitude < 0.5:
            self.stability_timer += dt
            if self.stability_timer >= 3.0:
                self.is_stable = True
                self.motion_active = False
        else:
            self.is_stable = False
            self.stability_timer = 0
            self.motion_active = True
            self.motion_cooldown = 0
        
        # Motion reactivation cooldown
        if self.motion_cooldown > 0:
            self.motion_cooldown -= dt
        
        if self.on_motion:
            self.on_motion(self.accel_x, self.accel_y, self.is_stable)


class LunarDriftApp(App):
    """Main Lunar Drift application."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Lunar Drift"
        self.sensor_manager = None
        self.moon_renderer = None
        self.settings_popup = None
        self.tap_time = 0
        self.tap_count = 0
        self.last_tap_x = 0
        self.last_tap_y = 0
        self.settings = self.load_settings()
        
    def build(self):
        """Build the application UI."""
        # Set window to full screen
        Window.fullscreen = 'auto'
        
        # Main layout
        main_layout = FloatLayout()
        
        # Moon renderer
        self.moon_renderer = MoonRenderer(size_hint=(1, 1))
        main_layout.add_widget(self.moon_renderer)
        
        # Initialize sensor manager
        self.sensor_manager = SensorManager(
            on_motion_callback=self.on_device_motion
        )
        
        # Schedule sensor updates
        Clock.schedule_interval(self.sensor_manager.update, 0.016)
        
        # Bind touch events for double-tap
        main_layout.bind(on_touch_down=self.on_touch_down)
        
        # Apply settings
        self.apply_settings()
        
        return main_layout
    
    def on_device_motion(self, x, y, is_stable):
        """Handle device motion sensor events."""
        if is_stable:
            # Freeze parallax when stable
            self.moon_renderer.parallax_x = 0
            self.moon_renderer.parallax_y = 0
        else:
            # Apply parallax based on device tilt
            max_parallax = min(self.root.width, self.root.height) * 0.1
            self.moon_renderer.parallax_x = x * max_parallax * 2
            self.moon_renderer.parallax_y = -y * max_parallax * 2
    
    def on_touch_down(self, instance, touch):
        """Handle touch events for double-tap detection."""
        current_time = datetime.now().timestamp()
        
        # Check for double-tap (within 300ms)
        if current_time - self.tap_time < 0.3:
            distance = np.sqrt((touch.x - self.last_tap_x)**2 + (touch.y - self.last_tap_y)**2)
            if distance < 50:  # Within 50 pixels
                self.on_double_tap()
                self.tap_count = 0
                return True
        
        self.tap_time = current_time
        self.last_tap_x = touch.x
        self.last_tap_y = touch.y
        self.tap_count += 1
        
        # Single tap opens settings menu
        if self.tap_count == 1:
            Clock.schedule_once(lambda dt: self.show_settings_menu(), 0.3)
        
        return True
    
    def on_double_tap(self):
        """Handle double-tap - trigger pulse animation."""
        self.moon_renderer.pulse_factor = 1.2
        Clock.schedule_once(lambda dt: setattr(self.moon_renderer, 'pulse_factor', 1.0), 0.3)
    
    def show_settings_menu(self):
        """Display settings popup menu."""
        if self.tap_count > 1:
            return  # Double-tap, don't show menu
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text='Lunar Drift Settings', size_hint_y=0.1, bold=True)
        content.add_widget(title)
        
        # Settings grid
        settings_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.8, padding=10)
        
        # Brightness slider
        settings_grid.add_widget(Label(text='Glow Intensity:', size_hint_x=0.4))
        glow_slider = Slider(min=0.3, max=1.5, value=self.settings.get('glow_intensity', 1.0))
        glow_slider.bind(value=self.on_glow_changed)
        settings_grid.add_widget(glow_slider)
        
        # Moon size slider
        settings_grid.add_widget(Label(text='Moon Size:', size_hint_x=0.4))
        size_slider = Slider(min=0.15, max=0.4, value=self.settings.get('moon_size', 0.25))
        size_slider.bind(value=self.on_size_changed)
        settings_grid.add_widget(size_slider)
        
        # Parallax toggle
        settings_grid.add_widget(Label(text='Parallax Effect:', size_hint_x=0.4))
        parallax_switch = Switch(active=self.settings.get('parallax_enabled', True))
        parallax_switch.bind(active=self.on_parallax_toggled)
        settings_grid.add_widget(parallax_switch)
        
        content.add_widget(settings_grid)
        
        # Close button
        close_btn = Button(text='Close Settings', size_hint_y=0.1)
        content.add_widget(close_btn)
        
        self.settings_popup = Popup(
            title='Lunar Drift Settings',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        close_btn.bind(on_press=self.settings_popup.dismiss)
        self.settings_popup.open()
    
    def on_glow_changed(self, instance, value):
        """Update glow intensity setting."""
        self.moon_renderer.glow_intensity = value
        self.settings['glow_intensity'] = value
        self.save_settings()
    
    def on_size_changed(self, instance, value):
        """Update moon size setting."""
        self.settings['moon_size'] = value
        self.save_settings()
    
    def on_parallax_toggled(self, instance, value):
        """Toggle parallax effect."""
        self.settings['parallax_enabled'] = value
        if not value:
            self.moon_renderer.parallax_x = 0
            self.moon_renderer.parallax_y = 0
        self.save_settings()
    
    def apply_settings(self):
        """Apply saved settings to the app."""
        if self.moon_renderer:
            self.moon_renderer.glow_intensity = self.settings.get('glow_intensity', 1.0)
    
    def load_settings(self):
        """Load settings from file."""
        settings_file = Path.home() / '.lunar_drift_settings.json'
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
        return {}
    
    def save_settings(self):
        """Save settings to file."""
        try:
            settings_file = Path.home() / '.lunar_drift_settings.json'
            with open(settings_file, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")


if __name__ == '__main__':
    app = LunarDriftApp()
    app.run()
