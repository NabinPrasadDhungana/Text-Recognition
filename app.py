#!/usr/bin/env python3
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

from preprocess import preprocess_image
from detector import detect_field_boxes
from ocr import ocr_image_region
from db import Database

def process_image(path, form_type=None, debug=False):
    img, pre = preprocess_image(path)
    boxes = detect_field_boxes(pre, debug=debug)

    results = []
    for i, (x, y, w, h) in enumerate(boxes):
        # Slightly pad the box for OCR
        pad = 4
        roi = img[max(y-pad,0):y+h+pad, max(x-pad,0):x+w+pad]
        text = ocr_image_region(roi)
        results.append({
            "box_index": i,
            "box": [int(x), int(y), int(w), int(h)],
            "text": text.strip()
        })

    # Assemble a simple key-value map: field_0..n
    data = {f"field_{r['box_index']}": r['text'] for r in results}

    # Save to DB
    db = Database()
    db.save_form(form_type=form_type or "unknown", image_path=path, data=data)
    print(f"Saved {len(results)} fields to DB.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan form image, extract fields, save to Postgres.")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--form-type", default=None, help="Optional form type")
    parser.add_argument("--debug", action="store_true", help="Show debug output (prints boxes)")
    args = parser.parse_args()
    process_image(args.image, form_type=args.form_type, debug=args.debug)