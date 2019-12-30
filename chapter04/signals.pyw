import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ZeroSpinBox(QSpinBox):

    zeros = 0
    atZero = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ZeroSpinBox, self).__init__(parent)
        self.valueChanged.connect(self.checkZero)

    def checkZero(self):
        if self.value() == 0:
            self.zeros += 1
            self.atZero.emit(self.zeros)

    def announce(self, zeros):
        print("ZeroSpinBox has been at zero %d times." % zeros)



class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        dial = QDial()
        dial.setNotchesVisible(True)
        spinbox = ZeroSpinBox()
        self.label = QLabel(str(spinbox.value()))

        layout = QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(spinbox)
        layout.addWidget(self.label)
        self.setLayout(layout)

        dial.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(dial.setValue)
        spinbox.atZero.connect(spinbox.announce)
        spinbox.valueChanged.connect(lambda: self.updateui(
            str(spinbox.value())))

        self.setWindowTitle("Signals and Slots")

    def updateui(self, x):
        self.label.setText(x)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
