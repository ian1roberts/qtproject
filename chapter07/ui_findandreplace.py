# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'findandreplacedlg.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FindAndReplaceDlg(object):
    def setupUi(self, FindAndReplaceDlg):
        FindAndReplaceDlg.setObjectName("FindAndReplaceDlg")
        FindAndReplaceDlg.resize(500, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FindAndReplaceDlg.sizePolicy().hasHeightForWidth())
        FindAndReplaceDlg.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        FindAndReplaceDlg.setFont(font)
        FindAndReplaceDlg.setSizeGripEnabled(False)
        self.line = QtWidgets.QFrame(FindAndReplaceDlg)
        self.line.setGeometry(QtCore.QRect(320, 20, 31, 161))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget = QtWidgets.QWidget(FindAndReplaceDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 284, 162))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.findwhatLabel = QtWidgets.QLabel(self.layoutWidget)
        self.findwhatLabel.setObjectName("findwhatLabel")
        self.gridLayout.addWidget(self.findwhatLabel, 0, 0, 1, 1)
        self.findWhatLineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.findWhatLineEdit.setObjectName("findWhatLineEdit")
        self.gridLayout.addWidget(self.findWhatLineEdit, 0, 1, 1, 1)
        self.replacewithLabel = QtWidgets.QLabel(self.layoutWidget)
        self.replacewithLabel.setObjectName("replacewithLabel")
        self.gridLayout.addWidget(self.replacewithLabel, 1, 0, 1, 1)
        self.replaceWithLineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.replaceWithLineEdit.setObjectName("replaceWithLineEdit")
        self.gridLayout.addWidget(self.replaceWithLineEdit, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.caseSensitiveCheckBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.caseSensitiveCheckBox.setChecked(False)
        self.caseSensitiveCheckBox.setObjectName("caseSensitiveCheckBox")
        self.horizontalLayout.addWidget(self.caseSensitiveCheckBox)
        self.wholeWordsCheckBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.wholeWordsCheckBox.setChecked(True)
        self.wholeWordsCheckBox.setObjectName("wholeWordsCheckBox")
        self.horizontalLayout.addWidget(self.wholeWordsCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.syntaxLabel = QtWidgets.QLabel(self.layoutWidget)
        self.syntaxLabel.setObjectName("syntaxLabel")
        self.horizontalLayout_2.addWidget(self.syntaxLabel)
        self.syntaxComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.syntaxComboBox.setObjectName("syntaxComboBox")
        self.syntaxComboBox.addItem("")
        self.syntaxComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.syntaxComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.layoutWidget1 = QtWidgets.QWidget(FindAndReplaceDlg)
        self.layoutWidget1.setGeometry(QtCore.QRect(370, 20, 99, 158))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.findButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.findButton.setObjectName("findButton")
        self.verticalLayout_2.addWidget(self.findButton)
        self.replaceButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.replaceButton.setObjectName("replaceButton")
        self.verticalLayout_2.addWidget(self.replaceButton)
        self.replaceAllButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.replaceAllButton.setObjectName("replaceAllButton")
        self.verticalLayout_2.addWidget(self.replaceAllButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.closeButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.closeButton.setObjectName("closeButton")
        self.verticalLayout_2.addWidget(self.closeButton)
        self.findwhatLabel.setBuddy(self.findWhatLineEdit)
        self.replacewithLabel.setBuddy(self.replaceWithLineEdit)
        self.syntaxLabel.setBuddy(self.syntaxComboBox)

        self.retranslateUi(FindAndReplaceDlg)
        self.closeButton.clicked.connect(FindAndReplaceDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(FindAndReplaceDlg)

    def retranslateUi(self, FindAndReplaceDlg):
        _translate = QtCore.QCoreApplication.translate
        FindAndReplaceDlg.setWindowTitle(_translate("FindAndReplaceDlg", "Find and Replace"))
        self.findwhatLabel.setText(_translate("FindAndReplaceDlg", "Find &What"))
        self.replacewithLabel.setText(_translate("FindAndReplaceDlg", "ReplaceW&ith"))
        self.caseSensitiveCheckBox.setText(_translate("FindAndReplaceDlg", "&Case Sensitive"))
        self.wholeWordsCheckBox.setText(_translate("FindAndReplaceDlg", "Wh&ole Words"))
        self.syntaxLabel.setText(_translate("FindAndReplaceDlg", "&Syntax"))
        self.syntaxComboBox.setItemText(0, _translate("FindAndReplaceDlg", "Literal Text"))
        self.syntaxComboBox.setItemText(1, _translate("FindAndReplaceDlg", "Regular Expressions"))
        self.findButton.setText(_translate("FindAndReplaceDlg", "&Find"))
        self.replaceButton.setText(_translate("FindAndReplaceDlg", "&Replace"))
        self.replaceAllButton.setText(_translate("FindAndReplaceDlg", "Replace &All"))
        self.closeButton.setText(_translate("FindAndReplaceDlg", "Close"))

