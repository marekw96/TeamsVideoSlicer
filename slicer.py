import cv2
from PIL import Image, ImageFilter
from SSIM_PIL import compare_ssim
from pathlib import Path


def frame_to_image(frame, image_area=None):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)

    if image_area is not None:
        x_start, y_start, x_stop, y_stop = image_area
        image = image.crop((x_start, y_start, x_stop, y_stop))

    return image


def preprocess_images(img):
    return img.convert('L') \
        .resize((32, 32), resample=Image.BICUBIC)


def are_two_images_different(lhs, rhs, threshold=0.93, print_value=False):
    lhs = preprocess_images(lhs)
    rhs = preprocess_images(rhs)

    value = compare_ssim(lhs, rhs, GPU=False)
    if print_value:
        print(value)
    return value < threshold


def get_output_path(file_path):
    file_path = file_path + "_output"
    return file_path


def make_output_dir(output_path):
    Path(output_path).mkdir(parents=True, exist_ok=True)


def save_image(output_path, name, image):
    print("Saved {}/{}.jpeg".format(output_path, name))
    image.save("{}/{}.jpeg".format(output_path, name), "JPEG")


def slice_video(file_path, starts_at=0, image_area=None):
    capture = cv2.VideoCapture(file_path)

    if not capture.isOpened():
        raise RuntimeError("Failed to open {}".format(file_path))

    frames_length = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("Total frames: {}".format(frames_length))
    output_path = get_output_path(file_path)
    make_output_dir(output_path)

    capture.set(cv2.CAP_PROP_POS_FRAMES, starts_at)

    ret, old_frame = capture.read()
    old_image = frame_to_image(old_frame, image_area)
    i = starts_at
    save_image(output_path, i, old_image)
    while ret:
        i += 1
        ret, new_frame = capture.read()
        if not ret:
            continue

        new_image = frame_to_image(new_frame, image_area)
        if are_two_images_different(old_image, new_image):
            save_image(output_path, i, new_image)
            old_image = new_image

        if i % 1000 == 0:
            print("Parsed {} frames. It's {}%".format(i, i / frames_length * 100))


def slice_video_dbg(file_path, starts_at=0, image_area=None):
    capture = cv2.VideoCapture(file_path)
    capture.set(cv2.CAP_PROP_POS_FRAMES, starts_at)
    ret, old_frame = capture.read()
    old_image = frame_to_image(old_frame, image_area)
    ret, old_frame2 = capture.read()
    old_image2 = frame_to_image(old_frame2, image_area)

    capture.set(cv2.CAP_PROP_POS_FRAMES, (8*60 + 3) * 30)
    ret, old_frame3 = capture.read()
    old_image3 = frame_to_image(old_frame3, image_area)
    print("1 and 2 - same", are_two_images_different(old_image, old_image2, print_value=True))
    print("1 and 3 - diff", are_two_images_different(old_image, old_image3, print_value=True))
    print("2 and 3 - diff", are_two_images_different(old_image2, old_image3, print_value=True))

    save_image(".", 1, old_image)
    save_image(".", 2, old_image2)
    save_image(".", 3, old_image3)


def save_frame(file_path, starts_at=0, image_area=None):
    capture = cv2.VideoCapture(file_path)
    if not capture.isOpened():
        raise RuntimeError("Failed to open {}".format(file_path))

    capture.set(cv2.CAP_PROP_POS_FRAMES, starts_at)
    ret, frame = capture.read()
    image = frame_to_image(frame, image_area)
    save_image(".", starts_at, image)


if __name__ == "__main__":
    area = (100, 50, 1000, 600)
    video = 'videos/2021-01-25 15-49-07.mkv'
    #save_frame(video, starts_at=10000)
    #save_frame(video, starts_at=10001, image_area=area)
    slice_video(video, starts_at=0, image_area=None)
    #slice_video_dbg("videos/9.11.mp4", starts_at=(7*60 * 30), image_area=(100,0, 1800, 960))
