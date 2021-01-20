from PySide2.QtWidgets import (QMainWindow, QStatusBar,
                               QGridLayout, QMenuBar,
                               QFileDialog, QAction,
                               QWidget, QLabel,
                               QLineEdit, QPushButton)
from PySide2.QtGui import QDoubleValidator, Qt
from Settings import Settings


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        settings = Settings()
        con = settings.printerSettings
        grid = QGridLayout()
        self.setLayout(grid)
        double_validator = QDoubleValidator()
        grid.addWidget(QLabel("Size:"), 0, 0)
        grid.addWidget(QLabel("x:"), 0, 2)
        self.bedSizeX = QLineEdit(con['bed_size_x'])
        self.bedSizeX.setValidator(double_validator)
        # bedSizeX.returnPressed.connect(self.set_bed_x)
        grid.addWidget(self.bedSizeX, 0, 3)

        grid.addWidget(QLabel("y:"), 1, 2)
        self.bedSizeY = QLineEdit(con['bed_size_y'])
        self.bedSizeY.setValidator(double_validator)
        # bedSizeX.returnPressed.connect(self.set_rot_x)
        grid.addWidget(self.bedSizeY, 1, 3)

        grid.addWidget(QLabel("Origin:"), 2, 0)
        grid.addWidget(QLabel("x:"), 2, 2)
        self.originX = QLineEdit(con['origin_x'])
        self.originX.setValidator(double_validator)
        # bedSizeX.returnPressed.connect(self.set_rot_x)
        grid.addWidget(self.originX, 2, 3)

        grid.addWidget(QLabel("y:"), 3, 2)
        self.originY = QLineEdit(con['origin_y'])
        self.originY.setValidator(double_validator)
        # bedSizeX.returnPressed.connect(self.set_rot_x)
        grid.addWidget(self.originY, 3, 3)

        okButton = QPushButton('save')
        okButton.clicked.connect(self.set_printer_settings)
        grid.addWidget(okButton, 4, 3)

    def set_printer_settings(self):
        settings = Settings()
        con = settings.printerSettings
        con['bed_size_x'] = self.bedSizeX.text()
        con['bed_size_y'] = self.bedSizeY.text()
        con['origin_x'] = self.originX.text()
        con['origin_y'] = self.originY.text()
        #global windowProvider
        # windowProvider.loadSettings()
