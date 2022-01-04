import os


class ShadowChangesToFiles:
    def __init__(self, video, output_path):
        self._video = video
        self._output_path = output_path + "_output"

        if not os.path.exists(self._output_path):
            os.mkdir(self._output_path)

    def saveFrame(self, position):
        image = self._video.getFrame(position, asQt=False)
        zeros_to_add = 9 - len(str(position))
        name = self._output_path + "/" + '0'*zeros_to_add + str(position) + ".jpeg"
        image.save(name)
        print("ShadowChangesToFiles", "saved", name)

    def deleteFrame(self, position):
        zeros_to_add = 9 - len(str(position))
        name = self._output_path + "/" + '0'*zeros_to_add + str(position) + ".jpeg"
        os.remove(name)
        print("ShadowChangesToFiles", "removed", name)