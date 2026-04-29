# utils/helpers.py

import os
from PIL import Image

def safe_image_open(path):
    """Safely open an image file."""
    try:
        return Image.open(path).convert("RGB")
    except Exception as e:
        print(f"Error opening image: {e}")
        return None


def split_image_paths(folder_path):
    """
    Returns a list of image file paths inside a folder.
    Supports .jpg, .jpeg, .png.
    """
    if not os.path.exists(folder_path):
        return []

    images = []
    for file in os.listdir(folder_path):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            images.append(os.path.join(folder_path, file))
    return images