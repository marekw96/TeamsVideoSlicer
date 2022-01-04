from PySide6 import QtCore, QtWidgets, QtGui

class PixmapLabel(QtWidgets.QWidget):
    clicked = QtCore.Signal(int)

    def __init__(self, pixmap, position, selected=None, *args, **kwargs):
        super(PixmapLabel, self).__init__(*args, **kwargs)

        self.pixmap = pixmap
        self.position = position

        self.layout = QtWidgets.QVBoxLayout()

        self.labelPosition = QtWidgets.QLabel(str(position))
        self.layout.addWidget(self.labelPosition)

        self.label = QtWidgets.QLabel()
        self.label.setPixmap(pixmap)
        if selected:
             self.label.setStyleSheet("QLabel { background-color : grey; color : blue; }")
        self.layout.addWidget(self.label)
        #self.label.mouseReleaseEvent.connect(self.onMouseReleaseEvent)

        self.setLayout(self.layout)

    def mouseReleaseEvent(self, ev):
        self.clicked.emit(self.position)