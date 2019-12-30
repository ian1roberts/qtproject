import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Form(QDialog):
    def  __init__(self, parent=None):
        super(Form, self).__init__(parent)

        button1 = QPushButton("one")
        button2 = QPushButton("two")
        button3 = QPushButton("three")
        button4 = QPushButton("four")
        button5 = QPushButton("five")
        self.label = QLabel("")

        layout = QHBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        layout.addWidget(button5)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("Buttons")

        button1.clicked.connect(self.anybutton)
        button2.clicked.connect(self.anybutton)
        button3.clicked.connect(self.anybutton)
        button4.clicked.connect(self.anybutton)
        button5.clicked.connect(self.anybutton)


    def anybutton(self):
        b = self.sender()
        if b is None or not isinstance(b, QPushButton):
            return
        self.label.setText("you clicked button '%s'" % b.text())


app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())
