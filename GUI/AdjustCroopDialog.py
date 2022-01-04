from PySide6 import QtCore, QtWidgets, QtGui

class AdjustCroopDialog(QtWidgets.QDialog):
    updateCroop = QtCore.Signal(int, int, int, int)

    def __init__(self, croop, *args, **kwargs):
        super(AdjustCroopDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Adjust croop settings")

        self.croop = croop

        (ltx, lty, rbx, rby) = croop

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.firstRow = QtWidgets.QHBoxLayout()
        self.leftTopXElementLayout = QtWidgets.QHBoxLayout()
        self.leftTopXElementLayout.addWidget(QtWidgets.QLabel("Left top X:"))
        self.ltxText = QtWidgets.QTextEdit(str(ltx))
        self.leftTopXElementLayout.addWidget(self.ltxText)
        self.firstRow.addLayout(self.leftTopXElementLayout)

        self.leftTopYElementLayout = QtWidgets.QHBoxLayout()
        self.leftTopYElementLayout.addWidget(QtWidgets.QLabel("Left top Y:"))
        self.ltyText = QtWidgets.QTextEdit(str(lty))
        self.leftTopYElementLayout.addWidget(self.ltyText)
        self.firstRow.addLayout(self.leftTopYElementLayout)
        self.layout.addLayout(self.firstRow)

        self.secondRow = QtWidgets.QHBoxLayout()
        self.rightBottomXElementLayout = QtWidgets.QHBoxLayout()
        self.rightBottomXElementLayout.addWidget(QtWidgets.QLabel("Right bottom X:"))
        self.rbxText = QtWidgets.QTextEdit(str(rbx))
        self.rightBottomXElementLayout.addWidget(self.rbxText)
        self.secondRow.addLayout(self.rightBottomXElementLayout)

        self.rightBottomYElementLayout = QtWidgets.QHBoxLayout()
        self.rightBottomYElementLayout.addWidget(QtWidgets.QLabel("Right bottom y:"))
        self.rbyText = QtWidgets.QTextEdit(str(rby))
        self.rightBottomYElementLayout.addWidget(self.rbyText)
        self.secondRow.addLayout(self.rightBottomYElementLayout)
        self.layout.addLayout(self.secondRow)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.ltxText.textChanged.connect(self.onValueChange)
        self.ltyText.textChanged.connect(self.onValueChange)
        self.rbxText.textChanged.connect(self.onValueChange)
        self.rbyText.textChanged.connect(self.onValueChange)

    def onValueChange(self):
        ltx = int(self.ltxText.toPlainText())
        lty = int(self.ltyText.toPlainText())
        rbx = int(self.rbxText.toPlainText())
        rby = int(self.rbyText.toPlainText())

        self.updateCroop.emit(ltx, lty, rbx, rby)

    def accept(self):
        ltx = int(self.ltxText.toPlainText())
        lty = int(self.ltyText.toPlainText())
        rbx = int(self.rbxText.toPlainText())
        rby = int(self.rbyText.toPlainText())

        self.croop = (ltx, lty, rbx, rby)

        self.hide()


    def reject(self):
        self.hide()