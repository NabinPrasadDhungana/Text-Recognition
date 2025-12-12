import cv2
import numpy as np

def preprocess_image(path, max_dim=1600):
    """
    Load image, resize keeping aspect ratio (to limit memory),
    return color image and preprocessed grayscale image for detection.
    """
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Could not load image {path}")

    h, w = img.shape[:2]
    scale = 1.0
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Smooth then adaptive threshold to handle lighting changes
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    th = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 1)
    # Morph close to join small gaps in boxes/lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5))
    closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
    return img, closed

# print(preprocess_image('form.png'))