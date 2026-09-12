#!/usr/bin/env python3
"""Icon generator for Lunar Drift"""
from PIL import Image, ImageDraw
import os

def create_icon(size=192, output_path="data/icon.png"):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = size // 8
    moon_bbox = [margin, margin, size - margin, size - margin]
    draw.ellipse(moon_bbox, fill=(240, 240, 230, 255))
    crater_size = size // 12
    craters = [(size // 3, size // 3, crater_size), (size // 2 + size // 8, size // 2, crater_size // 2)]
    for cx, cy, cr in craters:
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(200, 200, 190, 255))
    img.save(output_path)
    print(f"Created {output_path}")

def create_presplash(size=1280, output_path="data/presplash.png"):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img = Image.new('RGB', (size, size), (5, 5, 15))
    draw = ImageDraw.Draw(img)
    margin = size // 6
    moon_bbox = [margin, margin, size - margin, size - margin]
    draw.ellipse(moon_bbox, fill=(242, 242, 230))
    img.save(output_path)
    print(f"Created {output_path}")

if __name__ == '__main__':
    create_icon()
    create_presplash()
    print("Icons created successfully!")
