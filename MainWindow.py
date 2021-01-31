from PySide2.QtWidgets import (QMainWindow, QStatusBar,
                               QHBoxLayout, QMenuBar,
                               QFileDialog, QAction,
                               QWidget, QVBoxLayout,
                               QLabel, QSlider,
                               QGroupBox, QComboBox,
                               QDesktopWidget)
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QKeySequence
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
        contr.addSend("2d/image/opacity", self.opacityChangeSig)

        self.setAcceptDrops(True)

        mainWidgetsLayout = QHBoxLayout()
        mainWidgetsLayout.addWidget(ImageWidget())
        mainWidgetsLayout.addWidget(Model3dWidget())
        mainWidgetsLayout.addWidget(TabContainerWidget())
        groupbox = QGroupBox(self)
        groupbox.setLayout(mainWidgetsLayout)

        layout = QVBoxLayout()
        layout.addLayout(self.initTopBar())
        layout.addWidget(groupbox)
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
        #groupbox = QGroupBox(self)
        # groupbox.setLayout(layout)
        return layout

    # slider
    def initSlider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
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
    imageChangePathSig = Signal(str)
    imageChangeNameSig = Signal(str)
    homeViewSig = Signal()
    topViewSig = Signal()
    bottomViewSig = Signal()
    frontViewSig = Signal()
    backViewSig = Signal()
    leftViewSig = Signal()
    rightViewSig = Signal()

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addSend("3d/model/path", self.modelChangePathSig)
        contr.addSend("3d/model/name", self.modelChangeNameSig)
        contr.addSend("3d/camera/position/home", self.homeViewSig)
        contr.addSend("3d/camera/position/top", self.topViewSig)
        contr.addSend("3d/camera/position/bottom", self.bottomViewSig)
        contr.addSend("3d/camera/position/front", self.frontViewSig)
        contr.addSend("3d/camera/position/back", self.backViewSig)
        contr.addSend("3d/camera/position/left", self.leftViewSig)
        contr.addSend("3d/camera/position/right", self.rightViewSig)
        contr.addSend("2d/image/path", self.imageChangePathSig)
        contr.addSend("2d/image/name", self.imageChangeNameSig)

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

        file_menu.addAction(fileOpenAction)
        file_menu.addAction(exitAction)

        settingsOpenAction = QAction("Printer settings", self)
        settingsOpenAction.triggered.connect(self.openSettingsWindow)

        edit_menu.addAction(settingsOpenAction)

        homeView = QAction("Home", self)
        homeView.setShortcut(QKeySequence("0"))
        homeView.triggered.connect(self.homeViewSig.emit)
        topView = QAction("Top", self)
        topView.setShortcut(QKeySequence("1"))
        topView.triggered.connect(self.topViewSig.emit)
        bottomView = QAction("Bottom", self)
        bottomView.setShortcut(QKeySequence("2"))
        bottomView.triggered.connect(self.bottomViewSig.emit)
        frontView = QAction("Front", self)
        frontView.setShortcut(QKeySequence("3"))
        frontView.triggered.connect(self.frontViewSig.emit)
        backView = QAction("Back", self)
        backView.setShortcut(QKeySequence("4"))
        backView.triggered.connect(self.backViewSig.emit)
        leftView = QAction("Left", self)
        leftView.setShortcut(QKeySequence("5"))
        leftView.triggered.connect(self.leftViewSig.emit)
        rightView = QAction("Right", self)
        rightView.setShortcut(QKeySequence("6"))
        rightView.triggered.connect(self.rightViewSig.emit)

        view_menu.addAction(homeView)
        view_menu.addAction(topView)
        view_menu.addAction(bottomView)
        view_menu.addAction(frontView)
        view_menu.addAction(backView)
        view_menu.addAction(leftView)
        view_menu.addAction(rightView)

    def getfile(self):
        fname, tmp = QFileDialog.getOpenFileName(self, 'Open file',
                                                 '', "Model files (*.obj *.stl *.ply)")
        tmp = fname.rsplit('/', 1)
        self.modelChangeNameSig.emit(tmp[-1])
        self.modelChangePathSig.emit("file:///"+fname)
        self.statusBar.showMessage("Model loaded")

    def openSettingsWindow(self):
        self.sw = SettingsWindow(self)
        self.sw.setWindowModality(Qt.ApplicationModal)
        self.sw.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ingore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        fname = urls[0].toLocalFile()
        tmp = fname.rsplit('/', 1)
        name = tmp[-1]
        tmp = name.rsplit('.', 1)
        extension = tmp[-1].lower()
        supportedModelExtensions = ['obj', 'stl', 'ply']
        if any(extension in s for s in supportedModelExtensions):
            self.modelChangeNameSig.emit(name)
            self.modelChangePathSig.emit("file:///"+fname)
        else:
            self.imageChangeNameSig.emit(name)
            self.imageChangePathSig.emit(fname)
