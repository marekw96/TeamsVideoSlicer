import cv2
from PIL import Image, ImageQt

class VideoWrapper:
    def __init__(self, video_path):
        self._video = cv2.VideoCapture(video_path)

        if not self._video.isOpened():
            raise RuntimeError("Failed to open {}".format(video_path))

    def getTotalFramesNumber(self):
        return self._video.get(cv2.CAP_PROP_FRAME_COUNT)

    def getFrame(self, position, scale=None, asQt=True):
        self._video.set(cv2.CAP_PROP_POS_FRAMES, position)
        ret, frame = self._video.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)

        if scale:
            image.thumbnail(scale, Image.ANTIALIAS)

        if asQt:
            return ImageQt.ImageQt(image)
        else:
            return image

