from PIL import Image
import pytesseract
from connection import get_connection

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

extracted_text = extract_text_from_image('form2(1).jpeg')

multi_line_data = extracted_text.splitlines()

data = {}

for line in multi_line_data:
    line = line.strip()
    if ':' not in line:
        continue

    key, value = line.split(':', 1)
    data[key.strip()] = value.strip()

print(data)

conn = get_connection()
cur = conn.cursor()

values = ()

if not data:
    print("There is no data!")

else:
    print(data.values())
    print(cur)