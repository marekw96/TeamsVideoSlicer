from PySide6 import QtCore, QtWidgets, QtGui

from PixmapLabel import PixmapLabel

class PreviewSliderWidget(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(int)

    def __init__(self, video_handler, *args, **kwargs):
        super(PreviewSliderWidget, self).__init__(*args, **kwargs)

        self._video = video_handler

        self.layout = QtWidgets.QVBoxLayout()
        self.previewLayout = QtWidgets.QHBoxLayout()
        self.updatePreview(0)
        self.layout.addLayout(self.previewLayout)

        self.videoSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.videoSlider.setRange(0, self._video.getTotalFramesNumber())
        self.videoSlider.setSingleStep(1)
        self.videoSlider.setTickInterval(10)
        self.videoSlider.valueChanged.connect(self.onValueChanged)
        self.layout.addWidget(self.videoSlider)

        self.setLayout(self.layout)

    def updatePreview(self, position):
        for i in reversed(range(self.previewLayout.count())):
            self.previewLayout.itemAt(i).widget().setParent(None)

        totalFrames = self._video.getTotalFramesNumber()
        offsets = [-30* 60, -30 * 30, -30*10, 0, 30*10, 30*30, 30 * 60]
        for offset in offsets:
            previewPosition = position + offset
            if previewPosition < 0 or previewPosition >= totalFrames:
                continue

            pixmap = QtGui.QPixmap.fromImage(self._video.getFrame(previewPosition, (225,225)))
            pixmapLabel = PixmapLabel(pixmap, previewPosition, previewPosition == position)
            pixmapLabel.clicked.connect(self.onPreviewCliecked)
            self.previewLayout.addWidget(pixmapLabel)

    def scrollTo(self, position):
        self.onPreviewCliecked(position)

    @QtCore.Slot()
    def onPreviewCliecked(self, position):
        print(f"Preview clicked position: {position}")
        self.videoSlider.setValue(position)

    @QtCore.Slot()
    def onValueChanged(self, position):
        self.updatePreview(position)
        self.valueChanged.emit(position)
