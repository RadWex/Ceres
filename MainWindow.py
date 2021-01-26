from PySide2.QtWidgets import (QMainWindow, QStatusBar,
                               QHBoxLayout, QMenuBar,
                               QFileDialog, QAction,
                               QWidget, QVBoxLayout,
                               QLabel, QSlider,
                               QGroupBox, QComboBox,
                               QDesktopWidget, QDialog)
from PySide2.QtCore import Qt, Signal
from TabsContainer import TabContainerWidget
from SettingsWindow import SettingsWindow
from Viewer3d import Model3dWidget
from Viewer2d import ImageWidget
from Controller import Controller


class MainWidget(QWidget):
    opacityChangeSig = Signal(float)

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addSend("2d/opacity", self.opacityChangeSig)

        self.setAcceptDrops(True)

        mainWidgetsLayout = QHBoxLayout()
        mainWidgetsLayout.addWidget(ImageWidget())
        mainWidgetsLayout.addWidget(Model3dWidget())
        mainWidgetsLayout.addWidget(TabContainerWidget())

        layout = QVBoxLayout()
        layout.addWidget(self.initTopBar())
        layout.addLayout(mainWidgetsLayout)
        self.setLayout(layout)

    def initTopBar(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Opacity:"))
        layout.addWidget(self.initSlider())
        layout.addWidget(QLabel("Printer:"))
        layout.addWidget(self.initPrinterProfileComboBox())
        layout.addWidget(QLabel("Template:"))
        layout.addWidget(self.initEngravingProfileComboBox())
        layout.addStretch(1)
        groupbox = QGroupBox(self)
        groupbox.setLayout(layout)
        return groupbox

    # slider
    def initSlider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(100)
        # slider.setMaximumWidth(20)
        slider.valueChanged.connect(self.opacityChange)

        return slider

    def opacityChange(self, value):
        value = value / 100
        self.opacityChangeSig.emit(value)
    # end_of_slider

    # first_comboBox
    def initPrinterProfileComboBox(self):
        combo = QComboBox()
        combo.addItem("Default")
        combo.addItem("Add new profile...")
        return combo
    # end_of_first_comboBox

    # second_comboBox
    def initEngravingProfileComboBox(self):
        combo = QComboBox()
        combo.addItem("Default")
        combo.addItem("Add new template...")
        return combo
    # end_of_second_comboBox


class MainWindow(QMainWindow):
    modelChangePathSig = Signal(str)
    modelChangeNameSig = Signal(str)

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addSend("3d/model/path", self.modelChangePathSig)
        contr.addSend("3d/model/name", self.modelChangeNameSig)

        self.initialize_menu_bar()
        self.setWindowTitle("Ceres")
        self.setAcceptDrops(True)

        # status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # central widget
        mainWidget = MainWidget()
        self.setCentralWidget(mainWidget)
        # self.centerOnScreen()

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def initialize_menu_bar(self):
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("&File")
        edit_menu = menu_bar.addMenu("&Edit")
        view_menu = menu_bar.addMenu("&View")

        fileOpenAction = QAction("Open", self)
        fileOpenAction.triggered.connect(self.getfile)
        exitAction = QAction("Quit", self)
        exitAction.triggered.connect(qApp.quit)

        settingsOpenAction = QAction("Printer settings", self)
        settingsOpenAction.triggered.connect(self.openSettingsWindow)
        edit_menu.addAction(settingsOpenAction)
        file_menu.addAction(fileOpenAction)
        file_menu.addAction(exitAction)

    def getfile(self):
        fname, tmp = QFileDialog.getOpenFileName(self, 'Open file',
                                                 '', "Model files (*.obj *.stl *.ply)")
        tmp = fname.rsplit('/', 1)
        self.modelChangeNameSig.emit(tmp[-1])
        self.modelChangePathSig.emit("file:///"+fname)
        self.statusBar.showMessage("Model loaded")

    def openSettingsWindow(self):
        dialog = SettingsWindow(self)
        if dialog.exec_() == QDialog.Accepted:
            print('settings windwo')
        else:
            print('Cancelled')
        dialog.deleteLater()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ingore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        fname = urls[0].toLocalFile()
        tmp = fname.rsplit('/', 1)
        self.modelChangeNameSig.emit(tmp[-1])
        self.modelChangePathSig.emit("file:///"+fname)
