from PySide6 import QtCore, QtWidgets, QtGui

from PixmapLabel import PixmapLabel

class SelectedFrameItem(QtWidgets.QWidget):
    clicked = QtCore.Signal(int)
    requestRemove = QtCore.Signal(int)

    def __init__(self, position, pixmap, *args, **kwargs):
        super(SelectedFrameItem, self).__init__(*args, **kwargs)

        self.position = position

        self.layout = QtWidgets.QHBoxLayout()
        pixmapLabel = PixmapLabel(pixmap, position)
        pixmapLabel.clicked.connect(self.onItemClicked)
        self.layout.addWidget(pixmapLabel)

        self.removeButton = QtWidgets.QPushButton("X")
        self.removeButton.clicked.connect(self.onItemRemoveClicked)
        self.layout.addWidget(self.removeButton)

        self.setLayout(self.layout)

    @QtCore.Slot()
    def onItemClicked(self, position):
        print(f"SelectedFramesWidget clicked position: {position}")
        self.clicked.emit(position)

    @QtCore.Slot()
    def onItemRemoveClicked(self):
        self.requestRemove.emit(self.position)

class SelectedFramesWidget(QtWidgets.QWidget):
    clicked = QtCore.Signal(int)
    requestRemove = QtCore.Signal(int)

    def __init__(self, video_handler, selected_frames, *args, **kwargs):
        super(SelectedFramesWidget, self).__init__(*args, **kwargs)

        self._video = video_handler
        self._selectedFrames = selected_frames
        self.layout = QtWidgets.QVBoxLayout()

        self._generateView()

        self.setLayout(self.layout)

    def getFrames(self):
        return self._selectedFrames

    def _generateView(self):
        for frame in self._selectedFrames:
            pixmap = QtGui.QPixmap.fromImage(self._video.getFrame(frame, (225,225)))
            item = SelectedFrameItem(frame, pixmap)
            item.clicked.connect(self.onItemClicked)
            item.requestRemove.connect(self.onItemRemoveClicked)
            self.layout.addWidget(item)

    def removeItem(self, position):
        idInList = self._selectedFrames.index(position)
        self._selectedFrames.remove(position)
        self.layout.itemAt(idInList).widget().setParent(None)
        self.requestRemove.emit(position)

    def addItem(self, position):
        if position in self._selectedFrames:
            return

        self._selectedFrames.append(position)
        self._selectedFrames = sorted(self._selectedFrames)
        idInList = self._selectedFrames.index(position)

        pixmap = QtGui.QPixmap.fromImage(self._video.getFrame(position, (225,225)))
        item = SelectedFrameItem(position, pixmap)
        item.clicked.connect(self.onItemClicked)
        item.requestRemove.connect(self.onItemRemoveClicked)

        self.layout.insertWidget(idInList, item)


    @QtCore.Slot()
    def onItemClicked(self, position):
        print(f"SelectedFramesWidget clicked position: {position}")
        self.clicked.emit(position)

    @QtCore.Slot()
    def onItemRemoveClicked(self, position):
        print(f"SelectedFramesWidget remove position: {position}")
        self.removeItem(position)

    @QtCore.Slot()
    def onItemAddClicked(self, position):
        print(f"SelectedFramesWidget add position: {position}")
        self.addItem(position)