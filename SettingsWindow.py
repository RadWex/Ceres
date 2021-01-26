from PySide2.QtWidgets import (QMainWindow, QStatusBar,
                               QGridLayout, QMenuBar,
                               QFileDialog, QAction,
                               QWidget, QLabel,
                               QLineEdit, QPushButton,
                               QHBoxLayout, QVBoxLayout,
                               QGroupBox, QComboBox,
                               QDoubleSpinBox, QSizePolicy,
                               QDesktopWidget)
from PySide2.QtGui import QDoubleValidator, Qt
from PySide2.QtCore import Signal
from PySide2.QtGui import QImage, QPixmap
from Settings import Settings
from Controller import Controller
import sys


class SettingsWindow(QWidget):
    bedSizeChangeSig = Signal(float, float)

    def __init__(self, parent):
        super().__init__()
        contr = Controller()
        contr.addTempSend("3d/bedSize", self.bedSizeChangeSig)

        self.setWindowTitle("Printer Settings")

        settingsLayout = QVBoxLayout()
        settingsLayout.addWidget(self.initBedSettings())
        settingsLayout.addWidget(self.initLaserSettings())

        topLayout = QHBoxLayout()
        topLayout.addLayout(settingsLayout)
        label = QLabel(self)
        pixmap = QPixmap("icons/calibration.png")
        label.setPixmap(pixmap)
        topLayout.addWidget(label)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.initTopButtons())
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(self.initBottomButtons())
        self.setLayout(mainLayout)

    def initTopButtons(self):
        combo = QComboBox()
        combo.addItem("Default")
        combo.addItem("Add new profile...")
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalPolicy(QSizePolicy.Expanding)
        combo.setSizePolicy(sizePolicy)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Printer type:"))
        layout.addWidget(combo)
        layout.addWidget(QPushButton("Remove"))
        layout.addWidget(QPushButton("Export"))

        return layout

    def initBedSettings(self):
        settings = Settings()
        con = settings.printerSettings

        grid = QGridLayout()
        grid.addWidget(QLabel("Size:"), 0, 0)
        grid.addWidget(QLabel("x:"), 0, 2)
        self.bedSizeX = QDoubleSpinBox()
        self.bedSizeX.setRange(0, 99999)
        self.bedSizeX.setValue(float(con['bed_size_x']))
        grid.addWidget(self.bedSizeX, 0, 3)
        grid.addWidget(QLabel("mm"), 0, 4)

        grid.addWidget(QLabel("y:"), 1, 2)
        self.bedSizeY = QDoubleSpinBox()
        self.bedSizeY.setRange(0, 99999)
        self.bedSizeY.setValue(float(con['bed_size_y']))
        grid.addWidget(self.bedSizeY, 1, 3)
        grid.addWidget(QLabel("mm"), 1, 4)

        grid.addWidget(QLabel("Origin:"), 2, 0)
        grid.addWidget(QLabel("x:"), 2, 2)
        self.originX = QDoubleSpinBox()
        self.originX.setRange(0, 99999)
        self.originX.setValue(float(con['origin_x']))
        grid.addWidget(self.originX, 2, 3)
        grid.addWidget(QLabel("mm"), 2, 4)

        grid.addWidget(QLabel("y:"), 3, 2)
        self.originY = QDoubleSpinBox()
        self.originY.setRange(0, 99999)
        self.originY.setValue(float(con['origin_y']))
        grid.addWidget(self.originY, 3, 3)
        grid.addWidget(QLabel("mm"), 3, 4)

        grid.setColumnStretch(4, 1)

        groupbox = QGroupBox("Printer Settings")
        groupbox.setLayout(grid)
        return groupbox

    def initLaserSettings(self):
        settings = Settings()
        con = settings.laserSettings

        grid = QGridLayout()
        grid.addWidget(QLabel("W:"), 0, 0)
        bedSizeX = QDoubleSpinBox()
        bedSizeX.setRange(0, 99999)
        bedSizeX.setValue(float(con['w']))
        grid.addWidget(bedSizeX, 0, 1)

        grid.addWidget(QLabel("(H) Height for laser focus:"), 1, 0)
        bedSizeY = QDoubleSpinBox()
        bedSizeY.setRange(0, 99999)
        bedSizeY.setValue(float(con['h']))
        grid.addWidget(bedSizeY, 1, 1)

        grid.addWidget(QLabel("D:"), 2, 0)
        bedSizeZ = QDoubleSpinBox()
        bedSizeZ.setRange(0, 99999)
        bedSizeZ.setValue(float(con['d']))
        grid.addWidget(bedSizeZ, 2, 1)

        groupbox = QGroupBox("Laser Settings")
        groupbox.setLayout(grid)
        grid.setRowStretch(3, 1)
        grid.setColumnStretch(2, 1)
        return groupbox

    def initBottomButtons(self):
        addButton = QPushButton('Add')
        importButton = QPushButton('Import')
        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.set_printer_settings)
        cencelButton = QPushButton('Close')
        cencelButton.clicked.connect(self.close)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(addButton)
        buttonsLayout.addWidget(importButton)
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(saveButton)
        buttonsLayout.addWidget(cencelButton)
        return buttonsLayout

    def set_printer_settings(self):
        settings = Settings()
        con = settings.printerSettings
        bedX = self.bedSizeX.value()
        bedY = self.bedSizeY.value()
        con['bed_size_x'] = str(bedX)
        con['bed_size_y'] = str(bedY)
        con['origin_x'] = str(self.originX.text())
        con['origin_y'] = str(self.originY.text())
        self.bedSizeChangeSig.emit(float(bedX), float(bedY))
        self.bedSizeChangeSig.disconnect()
        settings.save()
        self.close()
