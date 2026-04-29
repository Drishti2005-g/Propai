import streamlit as st
from PIL import Image, ExifTags, ImageChops, ImageEnhance
import numpy as np
import io


def extract_exif(img):
    """Extract EXIF metadata from image"""
    try:
        exif = img._getexif()
        if not exif:
            return None

        exif_data = {}
        for tag, value in exif.items():
            key = ExifTags.TAGS.get(tag, tag)
            exif_data[key] = value
        return exif_data
    except:
        return None


def ela_img(image, quality=90):
    """Perform Error Level Analysis"""
    resaved = io.BytesIO()
    image.save(resaved, "JPEG", quality=quality)
    resaved_image = Image.open(resaved)

    ela = ImageChops.difference(image, resaved_image)
    enhancer = ImageEnhance.Brightness(ela)
    ela = enhancer.enhance(30)
    return ela


def analyze_image(img):
    """Simple fake detection logic"""

    issues = []

    # 1. EXIF check
    exif = extract_exif(img)
    if not exif:
        issues.append("no_metadata")

    # 2. ELA check (if too bright = suspicious)
    ela = ela_img(img)
    ela_array = np.array(ela)
    brightness = ela_array.mean()

    if brightness > 80:
        issues.append("high_ela")

    # 3. Sharpness check
    arr = np.array(img.convert("L"))
    sharpness = np.std(arr)
    if sharpness < 20:
        issues.append("too_smooth")

    # Final label
    if len(issues) == 0:
        result = "VERIFIED"
    elif len(issues) == 1:
        result = "SUSPICIOUS"
    else:
        result = "FAKE"

    return result, issues, exif, ela