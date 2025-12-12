import cv2
import numpy as np

def detect_field_boxes(binary_img, min_area=1000, max_area_ratio=0.9, debug=False):
    """
    Detect rectangular boxes in a preprocessed binary image (white on black),
    return list of bounding boxes (x,y,w,h). This is a simple heuristic:
    - find contours, approximate with polygons, keep rectangles.
    - filter by area and aspect ratio to try to pick fields.
    """
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h_img, w_img = binary_img.shape[:2]
    boxes = []
    print(len(contours))
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        x,y,w,h = cv2.boundingRect(cnt)
        if area > (w_img * h_img * max_area_ratio):
            continue
        # Filter very tall/thin or very small boxes, allow typical field shapes
        ar = w / (h + 1e-6)
        if ar < 0.3 and ar > 10:
            continue
        # Optionally approximate polygon and check for approx 4 sides
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) >= 4:
            boxes.append((x,y,w,h))

    # Optionally sort boxes top-to-bottom, left-to-right
    boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
    if debug:
        print(f"Detected {len(boxes)} candidate boxes.")
        for i,(x,y,w,h) in enumerate(boxes):
            print(f"  box {i}: x={x} y={y} w={w} h={h}")
    return boxes