from PySide6 import QtCore, QtWidgets, QtGui
import os

class Crooper(QtWidgets.QDialog):
    def __init__(self, video, selectedFrames, croop, videoPath, *args, **kwargs):
        super(Crooper, self).__init__(*args, **kwargs)

        self._video = video
        self._selectedFrames = selectedFrames
        self._croop = croop
        self._outputPath = videoPath + "_crooped"

        self.setWindowTitle("Crooping...")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Crooping, please wait..."))
        self.setLayout(self.layout)

        print("Crooper", "Writing to:", self._outputPath)

        if not os.path.exists(self._outputPath):
            os.mkdir(self._outputPath)

        for frame in selectedFrames:
            image = self._video.getFrame(frame, asQt=False)
            zeros_to_add = 9 - len(str(frame))
            name = self._outputPath + "/" + '0'*zeros_to_add + str(frame) + ".jpeg"
            image = image.crop(self._croop)
            image.save(name)

        self.close()




