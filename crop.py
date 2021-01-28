import os
from PIL import Image

files = os.listdir(os.getcwd())

for file in files:
    img = Image.open(file)
    img = img.crop((220, 115, 1085, 555))
    img.save(file)
    print(f"Cropped {file}")