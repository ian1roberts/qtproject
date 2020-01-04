import sys
import os
import platform
from PyQt5.QtCore import (Qt, QVariant, QSettings, QTimer, QSize, QPoint,
                          QFileInfo, QT_VERSION_STR, PYQT_VERSION_STR,
                          QFile)
from PyQt5.QtWidgets import (QSpinBox, QLabel, QApplication,
                             QMainWindow, QDockWidget, QListWidget,
                             QFrame, QAction, QActionGroup, QFileDialog,
                             QMessageBox, QInputDialog)
from PyQt5.QtGui import (QImage, QKeySequence, QIcon, QPixmap,
                         QImageWriter, QImageReader)
# import helpform
import qrc_resources
from newimagedlg import NewImageDlg

__version__ = "1.0.0"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False
        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imageLabel)

        logDockWidget = QDockWidget("Log", self)
        logDockWidget.setObjectName("logDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea |
                                      Qt.RightDockWidgetArea)
        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)

        self.printer = None
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)

        self.fileMenu = self.menuBar().addMenu("&File")
        editMenu = self.menuBar().addMenu("&Edit")
        helpMenu = self.menuBar().addMenu("&Help")

        fileNewAction = self.createAction("&New...", self.fileNew,
                                          QKeySequence.New,
                                          "filenew", "Create a new image")
        fileOpenAction = self.createAction("&Open...",
                                           self.fileOpen,
                                           QKeySequence.Open,
                                           "fileopen", "Open an image")
        fileSaveAction = self.createAction("&Save...", self.fileSave,
                                           QKeySequence.Save,
                                           "filesave", "Save an image")
        fileSaveAsAction = self.createAction("Save as...", self.fileSaveAs,
                                             None, "filesaveas",
                                             "Save an image under a new name")
        filePrintAction = self.createAction("&Print...", self.filePrint,
                                            QKeySequence.Print,
                                            "fileprint", "Print an image")
        fileQuitAction = self.createAction("&Quit", self.close,
                                           "Ctrl+Q", "filequit",
                                           "Close the application")
        editZoomAction = self.createAction("&Zoom...", self.editZoom,
                                           "Alt+Z", "editzoom",
                                           "Zoom the image")
        editInvertAction = self.createAction("&Invert", self.editInvert,
                                             "Ctrl+I", "editinvert",
                                             "Invert the image's colours",
                                             True, "toggled(bool)")
        editSwapAction = self.createAction("&Swap", self.editSwap,
                                           "Ctrl+A", "editswap",
                                           "Swap Red and Blue", True,
                                           "toggled(bool)")
        mirrorGroup = QActionGroup(self)
        editUnMirrorAction = self.createAction("&Unmirror", self.editUnMirror,
                                               "Ctrl+U", "editunmirror",
                                               "Unmirror the image",
                                               True, "toggled(bool)")
        mirrorGroup.addAction(editUnMirrorAction)
        editUnMirrorAction.setChecked(True)
        editMirrorHorizontallyAction = self.createAction(
                                         "Mirror &Horizontally",
                                         self.editMirrorHorizontally,
                                         "Ctrl+H", "editnmirrorhorizontally",
                                         "Mirror the image horizontally",
                                         True, "toggled(bool)")
        mirrorGroup.addAction(editMirrorHorizontallyAction)
        editMirrorVerticallyAction = self.createAction(
                                         "Mirror &Vertically",
                                         self.editMirrorVertically,
                                         "Ctrl+H", "editnmirrorVertically",
                                         "Mirror the image vertically",
                                         True, "toggled(bool)")
        mirrorGroup.addAction(editMirrorVerticallyAction)
        self.addActions(editMenu, (editInvertAction, editSwapAction,
                        editZoomAction))
        mirrorMenu = editMenu.addMenu(QIcon(":/editmirror.png"), "&Menu")
        self.addActions(mirrorMenu, (editUnMirrorAction,
                                     editMirrorHorizontallyAction,
                                     editMirrorVerticallyAction))

        helpHelpAction = self.createAction("&Help", self.helpHelp,
                                           "Alt+H", "helphelp",
                                           "User guide")
        helpAboutpAction = self.createAction("&About", self.helpAbout,
                                             "Alt+A", "helpabout",
                                             "About Image Changer")

        self.fileMenuActions = (fileNewAction, fileOpenAction, fileSaveAction,
                                fileSaveAsAction, None, filePrintAction,
                                fileQuitAction)
        self.fileMenu.aboutToShow.connect(self.updateFileMenu)

        self.addActions(helpMenu, (helpHelpAction, helpAboutpAction))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                        fileSaveAsAction))

        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editInvertAction, editSwapAction,
                        editUnMirrorAction, editMirrorHorizontallyAction,
                        editMirrorVerticallyAction))
        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
        self.zoomSpinBox.valueChanged.connect(self.showImage)
        editToolbar.addWidget(self.zoomSpinBox)

        separator = QAction(self)
        separator.setSeparator(True)
        self.addActions(self.imageLabel, (editInvertAction, editSwapAction,
                        editUnMirrorAction, separator,
                        editMirrorHorizontallyAction,
                        editMirrorVerticallyAction))

        self.resetableActions = ((editInvertAction, False),
                                 (editSwapAction, False),
                                 (editUnMirrorAction, True))
        settings = QSettings()
        self.recentFiles = settings.value("RecentFiles")
        size = settings.value("MainWindow/Size",
                              QVariant(QSize(600, 500)))
        self.resize(size)
        position = settings.value("MainWindow/Position",
                                  QVariant(QPoint(0, 0)))
        self.move(position)
        # self.restoreGeometry(settings.value("MainWindow/Geometry"))
        # self.restoreState(settings.value("MainWindow/State"))

        self.setWindowTitle("Image Changer")
        self.updateFileMenu()
        QTimer.singleShot(0, self.loadInitFile)

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            if signal == 'triggered()':
                action.triggered.connect(slot)
            else:
                action.toggled.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def loadInitFile(self):
        settings = QSettings()
        fname = settings.value("LastFile")
        if fname and QFile.exists(fname):
            self.loadFile(fname)

    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            filename = QVariant(self.filename) \
                if self.filename is not None else QVariant()
            settings.setValue('LastFile', filename)
            recentFiles = QVariant(self.recentFiles) \
                if self.recentFiles else QVariant()
            settings.setValue('RecentFiles', recentFiles)
            settings.setValue('MainWindow/Size', QVariant(self.size()))
            settings.setValue('MainWindow/Position', QVariant(self.pos()))
            settings.setValue("MainWindow/Geometry", QVariant(
                                          self.saveGeometry()))
            settings.setValue('MainWindow/State', QVariant(self.saveState()))
        else:
            event.ignore()

    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self,
                                         "Image Changer - Unsaved changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes | QMessageBox.No |
                                         QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.fileSave()
        return True

    def updateFileMenu(self):
        self.fileMenu.clear()
        self.addActions(self.fileMenu, self.fileMenuActions[:-1])
        current = self.filename if self.filename is not None else None
        recentFiles = []
        if self.recentFiles:
            for fname in self.recentFiles:
                if fname != current and QFile.exists(fname):
                    recentFiles.append(fname)

            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QAction(QIcon(":/icon.png"), "&%d %s" % (
                                i + 1, QFileInfo(fname).fileName()), self)
                action.setData(fname)
                action.triggered.connect(self.loadFile)
                self.fileMenu.addAction(action)

    def addRecentFile(self, fname):
        if fname is None:
            return
        if self.recentFiles is not None and fname in set(self.recentFiles):
            return
        if self.recentFiles is None:
            self.recentFiles = []
        self.recentFiles.insert(0, fname)
        while len(self.recentFiles) > 9:
            self.recentFiles.pop()

    def fileNew(self):
        if not self.okToContinue():
            return
        dialog = NewImageDlg(self)
        if dialog.exec_():
            self.addRecentFile(self.filename)
            self.image = QImage()
            for action, check in self.resetableActions:
                action.setChecked(check)
            self.image = dialog.image()
            self.filename = None
            self.dirty = True
            self.showImage()
            self.sizeLabel.setText("%d x %d" % (self.image.width(),
                                   self.image.height()))
            self.updateStatus("Created new image")

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        self.listWidget.addItem(message)
        if self.filename is not None:
            self.setWindowTitle("Image Changer - %s[*]" %
                                os.path.basename(self.filename))
        elif not self.image.isNull():
            self.setWindowTitle("Image Changer - Unnamed[*]")
        else:
            self.setWindowTitle("Image Changer[*]")
        self.setWindowModified(self.dirty)
        print(self.windowTitle())
        self.repaint()

    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = os.path.dirname(self.filename) \
            if self.filename is not None else "."
        formats = ["*.%s" % format.data().decode('ascii').lower()
                   for format in QImageReader.supportedImageFormats()]
        fname = QFileDialog.getOpenFileName(self,
                                            "Image Changer - Choose Image",
                                            dir, "Image files (%s)" %
                                            " ".join(formats))
        fname = fname[0]
        if fname:
            self.loadFile(fname)

    def loadFile(self, fname=None):
        if not fname:
            action = self.sender()
            if isinstance(action, QAction):
                fname = action.data()
                if not self.okToContinue():
                    return
            else:
                return
        if fname:
            self.filename = None
            image = QImage(fname)
            if image.isNull():
                message = "Failed to read %s" % fname
            else:
                self.addRecentFile(fname)
                self.image = QImage()
                for action, check in self.resetableActions:
                    action.setChecked(check)
                self.image = image
                self.filename = fname
                self.showImage()
                self.dirty = False
                self.sizeLabel.setText("%d x %d" % (
                                        image.width(), image.height()))
                message = "Loaded %s" % os.path.basename(fname)
            self.updateStatus(message)

    def fileSave(self):
        if self.image.isNull():
            return
        if self.filename is None:
            self.fileSaveAs()
        else:
            if self.image.save(self.filename, None):
                self.updateStatus("Saved as %s" % self.filename)
                self.dirty = False
            else:
                self.updateStatus("Failed to save %s" % self.filename)

    def fileSaveAs(self):
        if self.image.isNull():
            return
        fname = self.filename if self.filename is not None else "."
        formats = ["*.%s" % format.data().decode('ascii').lower()
                   for format in QImageWriter.supportedImageFormats()]
        fname = QFileDialog.getSaveFileName(self,
                                            "Image Changer - Save Image",
                                            fname, "Image files (%s)" %
                                            " ".join(formats))
        fname = fname[0]
        if fname:
            if "." not in fname:
                fname += ".png"
            self.addRecentFile(fname)
            self.filename = fname
            self.fileSave()

    def filePrint(self):
        pass

    def editInvert(self, on):
        if self.image.isNull():
            return
        self.image.invertPixels()
        self.dirty = True
        self.showImage()
        self.updateStatus("Inverted" if on else "Uninverted")

    def editSwap(self, on):
        if self.image.isNull():
            return
        self.image.rgbSwapped()
        self.dirty = True
        self.showImage()
        self.updateStatus("Red and blue pixels swapped" if on
                          else "Red and blue pixels restored")

    def editMirrorHorizontally(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(True, False)
        self.showImage()
        self.mirroredhorizontally = not self.mirroredhorizontally
        self.dirty = True
        self.updateStatus("Mirrored Horizontally"
                          if on else "Unmirrored Horizontally")

    def editMirrorVertically(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(False, True)
        self.showImage()
        self.mirroredvertically = not self.mirroredvertically
        self.dirty = True
        self.updateStatus("Mirrored Vertically"
                          if on else "Unmirrored Vertically")

    def editUnMirror(self, on):
        if self.image.isNull():
            return
        if self.mirroredhorizontally:
            self.editMirroredHorizontally(False)
        if self.mirroredvertically:
            self.editVertically(False)

    def editZoom(self):
        if self.image.isNull():
            return
        percent, ok = QInputDialog.getInteger(self, "Image Changer - Zoom",
                                              "Percent",
                                              self.zoomSpinBox.value(),
                                              1, 400)
        if ok:
            self.zoomSpinBox.setValue(percent)

    def showImage(self, percent=None):
        if self.image.isNull():
            return
        if percent is None:
            percent = self.zoomSpinBox.value()
        factor = percent / 100.0
        width = self.image.width() * factor
        height = self.image.height() * factor
        image = self.image.scaled(width, height, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

    def helpAbout(self):
        QMessageBox.about(self, "About Image Changer",
                          """<b>Image Changer</b> v %s
                             <p>Copyright &copy; 2007 Qtrac Ltd.
                             All rights reserved.
                             <p>This application can be used to provide simple
                             image manipulations.
                             <p>Python %s - Qt %s - PyQt %s on %s
                           """ % (__version__, platform.python_version(),
                                  QT_VERSION_STR, PYQT_VERSION_STR,
                                  platform.system()))

    def helpHelp(self):
        QMessageBox.warning(self, "Unimplemented Method",
                            """<b>Image Checker Help is unimplemented</b>""",
                            None)


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
