#!/usr/bin/env python3
"""
Simple script to upload local images to Render via admin interface
"""
import os
import shutil
from pathlib import Path

def copy_local_image():
    """Copy local image to match expected filename"""
    local_image = Path("backend/media/products/4.jpg")
    target_image = Path("backend/media/products/code_extra.png")
    
    if local_image.exists():
        # Convert JPG to PNG filename (you'll need to upload via admin)
        print(f"Found local image: {local_image}")
        print(f"You need to upload this as: code_extra.png")
        print(f"Go to: https://entstores.onrender.com/admin/shop/product/")
        print(f"Edit the 'jhj' product and upload the image: {local_image.absolute()}")
        return True
    else:
        print("No local image found")
        return False

if __name__ == "__main__":
    copy_local_image()