from PySide6 import QtCore, QtWidgets, QtGui

class FrameWidget(QtWidgets.QWidget):
    requestAdd = QtCore.Signal(int)

    def __init__(self, video_handler, croop, *args, **kwargs):
        super(FrameWidget, self).__init__(*args, **kwargs)

        self._position = 0
        self._video = video_handler
        self._croop = croop

        self.layout = QtWidgets.QVBoxLayout()
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.numberLabel = QtWidgets.QLabel(str(0))
        self.headerLayout.addWidget(self.numberLabel)

        self.addButton = QtWidgets.QPushButton("+")
        self.addButton.clicked.connect(self.onAddRequestClicked)
        self.headerLayout.addWidget(self.addButton)
        self.layout.addLayout(self.headerLayout)

        self.framePreviewLabel = QtWidgets.QLabel()
        self.layout.addWidget(self.framePreviewLabel)
        self.setLayout(self.layout)

        self.showFrame(0)

    @QtCore.Slot()
    def showFrame(self, position):
        self._position = position
        self.numberLabel.setText(str(position))
        self.framePreview = QtGui.QPixmap.fromImage(self._video.getFrame(position))
        #self.framePreviewLabel.setPixmap(self.framePreview)
        self.drawRectangle()

    @QtCore.Slot()
    def onAddRequestClicked(self):
        self.requestAdd.emit(self._position)

    def updateCroop(self, croop):
        self._croop = croop
        self.showFrame(self._position)

    def drawRectangle(self):
        (ltx, lty, rbx, rby) = self._croop

        self.framePreview = QtGui.QPixmap.fromImage(self._video.getFrame(self._position))
        painter = QtGui.QPainter (self.framePreview)
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 3))
        painter.drawLine(ltx, lty, ltx, rby)
        painter.drawLine(ltx, lty, rbx, lty)
        painter.drawLine(rbx, lty, rbx, rby)
        painter.drawLine(ltx, rby, rbx, rby)
        self.framePreviewLabel.setPixmap(self.framePreview)
