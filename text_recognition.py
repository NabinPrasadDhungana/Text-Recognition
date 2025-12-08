from PIL import Image
import pytesseract

# Specify the path to the Tesseract executable (if not in PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

image_file = 'path/to/your/image.png'
extracted_text = extract_text_from_image(image_file)
print(f"Extracted text: {extracted_text}")