import sys
import csv
from urllib.request import urlopen
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        date = self.getdata()
        rates = sorted(self.rates.keys())

        dateLabel = QLabel(date)
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 100000.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)
        self.toLabel = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)

        self.fromComboBox.currentIndexChanged.connect(self.updateUi)
        self.toComboBox.currentIndexChanged.connect(self.updateUi)
        self.fromSpinBox.valueChanged.connect(self.updateUi)
        self.setWindowTitle('Currency')

    def updateUi(self):
        to_ = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()
        amount = (self.rates[from_] / self.rates[to_]) \
            * self.fromSpinBox.value()
        self.toLabel.setText("%0.2f" % amount)

    def getdata(self):
        self.rates = {}

        try:
            fh = csv.reader(open('data/fxdata.csv'))
            date = "unknown"

            for line in fh:
                print(line)
                if len(line) != 2:
                    continue
                key, value = line
                if key.startswith("YYY"):
                    date = value
                else:
                    try:
                        value = float(value)
                        key = key.split('/')
                        self.rates[key[0]] = value
                    except ValueError:
                        pass
            return "Exchange Rates Date: " + date
        except Exception as e:
            return "Failed to download:\n%s" % eval


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
