import easyocr
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
result = reader.readtext('form.png', detail=0)
result = reader.readtext('image.png', detail=0)

print(result)