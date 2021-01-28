from PIL import Image
import os
from slicer import make_output_dir, are_two_images_different,save_image


def remove_duplicates(where):
    output_dir = where+"_unique"
    make_output_dir(output_dir)
    files = sorted(os.listdir(where))
    files_images = []
    saved_images = []

    for file in files:
        files_images.append({"name": file, "image": Image.open("{}/{}".format(where, file))})

    for index, lhs in enumerate(files_images):
        is_unique = True
        for rhs_index, rhs in enumerate(saved_images):
            if lhs["name"] == rhs["name"]:
                continue

            if not are_two_images_different(lhs["image"], rhs["image"]):
                is_unique = False
                print(f"{index}: {lhs['name']} is copy of {rhs['name']}")
                break

        if is_unique:
            saved_images.append(lhs)
            save_image(output_dir, lhs['name'].split('.')[0], lhs["image"])


if __name__ == "__main__":
    video = 'videos/2021-01-18 10-12-07.mkv_output'
    remove_duplicates(video)