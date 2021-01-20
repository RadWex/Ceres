from PySide2.QtWidgets import (QMainWindow, QStatusBar,
                               QHBoxLayout, QMenuBar,
                               QFileDialog, QAction,
                               QWidget)

from TabsContainer import TabContainerWidget
from SettingsWindow import SettingsWindow
from Viewer3d import Model3dWidget
from Viewer2d import ImageWidget


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.addWidget(ImageWidget())
        layout.addWidget(Model3dWidget())
        layout.addWidget(TabContainerWidget())
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        mainWidget = MainWidget()
        self.setCentralWidget(mainWidget)
        self.initialize_menu_bar()
        self.setWindowTitle("Ceres")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def initialize_menu_bar(self):
        self.sw = SettingsWindow()
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("&File")
        edit_menu = menu_bar.addMenu("&Edit")
        view_menu = menu_bar.addMenu("&View")
        exitAction = QAction("Quit", self)
        exitAction.triggered.connect(qApp.quit)
        fileOpenAction = QAction("Open", self)
        fileOpenAction.triggered.connect(self.getfile)
        settingsOpenAction = QAction("Printer settings", self)
        settingsOpenAction.triggered.connect(self.openSettingsWindow)
        edit_menu.addAction(settingsOpenAction)
        file_menu.addAction(fileOpenAction)
        file_menu.addAction(exitAction)

    def getfile(self):
        fname, tmp = QFileDialog.getOpenFileName(self, 'Open file',
                                                 'c:\\', "Model files (*.obj *.stl *.ply)")
        print(fname)
        #global provider
        #provider.modelChange = "file:///"+fname
        #provider.modelName = fname

    def openSettingsWindow(self):
        self.sw = SettingsWindow()
        self.sw.show()
