import os
import pytesseract
from PIL import Image
import numpy as np
import cv2

TESSERACT_CMD = os.getenv("TESSERACT_CMD")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# Basic OCR on an image region (BGR or grayscale numpy array)
def ocr_image_region(region_img, lang="eng"):
    if region_img is None or region_img.size == 0:
        return ""
    # Convert to PIL Image
    if isinstance(region_img, np.ndarray):
        if len(region_img.shape) == 3:
            rgb = cv2.cvtColor(region_img, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
        else:
            pil = Image.fromarray(region_img)
    else:
        pil = region_img

    # Basic config: treat as a single text line/word block; tune as needed
    config = "--psm 6"  # assume a uniform block of text
    text = pytesseract.image_to_string(pil, lang=lang, config=config)
    # quick cleaning
    text = text.replace("\r", " ").replace("\n", " ").strip()
    return text