import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui

from VideoWrapper import VideoWrapper
from FrameWidget import FrameWidget
from PreviewSliderWidget import PreviewSliderWidget
from SelectedFramesWidget import SelectedFramesWidget
from AdjustCroopDialog import AdjustCroopDialog
from Crooper import Crooper
from ShadowChangesToFiles import ShadowChangesToFiles

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("TeamsVideoSlcier")
        self.croop = (0,0, 100, 100)

        self._selectedFrames = []

        self.layout = QtWidgets.QVBoxLayout(self)
        self._video_path = "C:\\Users\\Marek\\Downloads\\TeamsVideoSlicer-master\\videos\\2021-10-22 07-54-36.mkv"
        self.loadFramesAlreadyParsed(self._video_path)
        self.video = VideoWrapper(self._video_path)

        self.shadowChanges = ShadowChangesToFiles(self.video, self._video_path)

        self.topBox = QtWidgets.QHBoxLayout()
        self.leftBox = QtWidgets.QVBoxLayout()
        self.selectedFramesWidget = SelectedFramesWidget(self.video, self._selectedFrames)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.selectedFramesWidget)
        self.leftBox.addWidget(self.scrollArea)

        self.rightBox = QtWidgets.QGridLayout()

        self.framePreview = FrameWidget(self.video, self.croop)
        self.rightBox.addWidget(self.framePreview)

        self.topBox.addLayout(self.leftBox, 1)
        self.topBox.addLayout(self.rightBox, 3)
        self.layout.addLayout(self.topBox, 3)

        self.bottomBox = QtWidgets.QVBoxLayout()
        self.videoSlider = PreviewSliderWidget(self.video)
        self.bottomBox.addWidget(self.videoSlider)
        self.layout.addLayout(self.bottomBox, 1)

        self.selectedFramesWidget.clicked.connect(self.videoSlider.scrollTo)
        self.framePreview.requestAdd.connect(self.selectedFramesWidget.onItemAddClicked)
        self.videoSlider.valueChanged.connect(self.framePreview.showFrame)

        self.selectedFramesWidget.requestRemove.connect(self.shadowChanges.deleteFrame)
        self.framePreview.requestAdd.connect(self.shadowChanges.saveFrame)

    def loadFramesAlreadyParsed(self, video_path):
        dir_path = video_path + "_output"
        files = os.listdir(dir_path)
        self._selectedFrames = [int(f.split(".")[0]) for f in files]

    def onCroopChangeInTime(self, ltx, lty, rbx, rby):
        print(ltx, lty, rbx, rby)
        temp_croop = (ltx, lty, rbx, rby)
        self.framePreview.updateCroop(temp_croop)

    def showCroopMenuPositionsDialog(self):
        print("showCroopMenuPositionsDialog")
        self.adjustCroopDialog = AdjustCroopDialog(self.croop)
        self.adjustCroopDialog.updateCroop.connect(self.onCroopChangeInTime)

        self.adjustCroopDialog.show()
        self.adjustCroopDialog.exec()
        self.croop = self.adjustCroopDialog.croop
        self.framePreview.updateCroop(self.croop)

        print("Update croop as", self.croop)

    def runCroopingDialog(self):
        print("runCroopingDialog")
        crooper = Crooper(self.video, self.selectedFramesWidget.getFrames(), self.croop, self._video_path)
        crooper.show()
        #crooper.exec()
        crooper.hide()
        print("Done")

class MainApplicationWrapper(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApplicationWrapper, self).__init__()
        self.setWindowTitle("TeamsVideoSlcier")

        mainWidget = MainWidget()
        self.setCentralWidget(mainWidget)

        menuBar = self.menuBar()
        croopMenuPositions = menuBar.addMenu("Croop")
        adjustAction = QtGui.QAction("Adjust croop", self)
        adjustAction.triggered.connect(mainWidget.showCroopMenuPositionsDialog)
        croopMenuPositions.addAction(adjustAction)

        runCroop = QtGui.QAction("Run croop", self)
        runCroop.triggered.connect(mainWidget.runCroopingDialog)
        croopMenuPositions.addAction(runCroop)

        self.showMaximized()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainApplicationWrapper()
    widget.show()

    sys.exit(app.exec())