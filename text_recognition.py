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

if not conn:
    print("Database connection error!")
else:
    try:
        with conn:
            with conn.cursor() as cur:

                columns = ['first_name', 'middle_name', 'last_name', 'age', 'college', 'program', 'semester']
                values = [data.get(col.replace('_', ' ').title(), '') for col in columns]
                query = "INSERT INTO form ({}) values({})".format(
                    ', '.join(columns),
                    ', '.join(['%s'] * len(values))
                )

                cur.execute(query, values)
                print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()