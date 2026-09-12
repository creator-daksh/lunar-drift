#!/usr/bin/env python3
"""Generate placeholder icons and presplash for Lunar Drift"""
from PIL import Image, ImageDraw
import os

def create_icons():
    """Create icon images for the app"""
    os.makedirs('data', exist_ok=True)
    
    # Icon sizes needed for Android
    sizes = [192]  # buildozer uses this primary size
    
    for size in sizes:
        img = Image.new('RGBA', (size, size), (5, 5, 15, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw moon
        margin = int(size * 0.1)
        radius = int((size - margin * 2) / 2)
        cx = size // 2
        cy = size // 2
        
        # Moon body (white)
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            fill=(242, 242, 230, 255)
        )
        
        # Craters
        crater_data = [
            (int(cx - radius * 0.3), int(cy - radius * 0.3), int(radius * 0.15)),
            (int(cx + radius * 0.2), int(cy + radius * 0.15), int(radius * 0.1)),
            (int(cx - radius * 0.1), int(cy + radius * 0.35), int(radius * 0.12)),
        ]
        
        for cx_c, cy_c, cr in crater_data:
            draw.ellipse(
                [cx_c - cr, cy_c - cr, cx_c + cr, cy_c + cr],
                fill=(200, 200, 190, 200)
            )
        
        # Glow
        glow_radius = int(radius * 1.2)
        draw.ellipse(
            [cx - glow_radius, cy - glow_radius, cx + glow_radius, cy + glow_radius],
            outline=(255, 255, 200, 100),
            width=2
        )
        
        img.save(f'data/icon.png')
        print(f"Created data/icon.png ({size}x{size})")

def create_presplash():
    """Create presplash/splash screen"""
    os.makedirs('data', exist_ok=True)
    
    width, height = 1280, 1280
    img = Image.new('RGB', (width, height), (5, 5, 15))
    draw = ImageDraw.Draw(img)
    
    # Draw moon in center
    margin = width // 6
    cx = width // 2
    cy = height // 2
    radius = (width - margin * 2) // 2
    
    # Moon body
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=(242, 242, 230)
    )
    
    # Craters
    crater_data = [
        (int(cx - radius * 0.3), int(cy - radius * 0.3), int(radius * 0.15)),
        (int(cx + radius * 0.2), int(cy + radius * 0.15), int(radius * 0.1)),
        (int(cx - radius * 0.1), int(cy + radius * 0.35), int(radius * 0.12)),
    ]
    
    for cx_c, cy_c, cr in crater_data:
        draw.ellipse(
            [cx_c - cr, cy_c - cr, cx_c + cr, cy_c + cr],
            fill=(200, 200, 190)
        )
    
    img.save('data/presplash.png')
    print("Created data/presplash.png")

if __name__ == '__main__':
    create_icons()
    create_presplash()
    print("\nIcon generation complete!")
