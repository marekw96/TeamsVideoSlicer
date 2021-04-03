import os
from PIL import Image
import sys


def main():
    if len(sys.argv) != 5:
        print("Provide 4 arguments")
        exit(1)

    files = os.listdir(os.getcwd())

    for file in files:
        img = Image.open(file)
        img = img.crop((int(sys.argv[1]), int(sys.argv[2]),
                        int(sys.argv[3]), int(sys.argv[4])))
        img.save(file)
        print(f"Cropped {file}")


if __name__ == "__main__":
    main()