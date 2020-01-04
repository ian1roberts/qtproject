from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import (QSpinBox, QLabel, QComboBox,
                             QDialog, QPushButton, QHBoxLayout, QGridLayout,
                             QColorDialog)
from PyQt5.QtGui import QPixmap, QBrush, QPainter


class NewImageDlg(QDialog):

    def __init__(self, parent=None):
        super(NewImageDlg, self).__init__(parent)

        widthLabel = QLabel("&Width:")
        self.widthSpinBox = QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.widthSpinBox.setRange(0, 500)
        self.widthSpinBox.setValue(250)
        heightLabel = QLabel("&Height:")
        self.heightSpinBox = QSpinBox()
        heightLabel.setBuddy(self.heightSpinBox)
        self.heightSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.heightSpinBox.setRange(0, 500)
        self.heightSpinBox.setValue(250)
        brushLabel = QLabel("&Brush pattern:")
        self.brushComboBox = QComboBox()
        brushLabel.setBuddy(self.brushComboBox)

        for value, text in (
                (Qt.SolidPattern, "Solid"),
                (Qt.Dense1Pattern, "Dense #1"),
                (Qt.Dense2Pattern, "Dense #2"),
                (Qt.Dense3Pattern, "Dense #3"),
                (Qt.Dense4Pattern, "Dense #4"),
                (Qt.Dense5Pattern, "Dense #5"),
                (Qt.Dense6Pattern, "Dense #6"),
                (Qt.Dense7Pattern, "Dense #7"),
                (Qt.HorPattern, "Horizontal"),
                (Qt.VerPattern, "Vertical"),
                (Qt.CrossPattern, "Cross"),
                (Qt.BDiagPattern, "Backward Diagonal"),
                (Qt.FDiagPattern, "Forward Diagonal"),
                (Qt.DiagCrossPattern, "Diagonal Cross")):
            self.brushComboBox.addItem(text, QVariant(value))
        self.brushComboBox.setCurrentIndex(0)

        cLabel = QLabel("Color")
        self.colorLabel = QLabel()
        self.color = Qt.red

        colorButton = QPushButton("&Color")
        okButton = QPushButton("&OK")
        cancelButton = QPushButton("Cancel")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        layout = QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(heightLabel, 1, 0)
        layout.addWidget(self.heightSpinBox, 1, 1)
        layout.addWidget(brushLabel, 2, 0)
        layout.addWidget(self.brushComboBox, 2, 1)
        layout.addWidget(cLabel, 3, 0)
        layout.addWidget(self.colorLabel, 3, 1)
        layout.addWidget(colorButton, 3, 2)
        layout.addLayout(buttonLayout, 4, 2)
        self.setLayout(layout)

        colorButton.clicked.connect(self.getColor)
        cancelButton.clicked.connect(self.reject)
        okButton.clicked.connect(self.accept)
        self.brushComboBox.currentIndexChanged.connect(self.setColor)
        self.setColor()

    def getColor(self):
        color = QColorDialog.getColor(Qt.black, self)
        if color.isValid():
            self.color = color
            self.setColor()

    def setColor(self):
        pixmap = self._makePixmap()
        self.colorLabel.setPixmap(pixmap)

    def image(self):
        pixmap = self._makePixmap(self.widthSpinBox.value(),
                                  self.heightSpinBox.value())
        return QPixmap.toImage(pixmap)

    def _makePixmap(self, width=60, height=30):
        pixmap = QPixmap(width, height)
        style = self.brushComboBox.itemData(
                self.brushComboBox.currentIndex())
        brush = QBrush(self.color, Qt.BrushStyle(style))
        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(), Qt.white)
        painter.fillRect(pixmap.rect(), brush)
        return pixmap
