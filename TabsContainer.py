from PySide2.QtWidgets import (QWidget, QVBoxLayout,
                               QTabWidget, QPushButton,
                               QLabel, QPlainTextEdit,
                               QFileDialog, QGridLayout,
                               QLayout, QGroupBox,
                               QLineEdit)
from PySide2.QtGui import QIntValidator
from PySide2.QtCore import Qt, Signal, QBuffer
from PIL import ImageEnhance, Image
from PIL.ImageQt import ImageQt
from SettingsWindow import SettingsWindow
from Settings import Settings
from ModelManipulation import ModelManipulation
from ImageManipulation import ImageManipulation
from Controller import Controller
import io
import numpy as np


class LaserManipulation(QWidget):
    object_gcode = ''
    x_offset = 0
    y_offset = 0
    image = None

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addRecive("2d/image", self.set_image)
        contr.addRecive("2d/image/location/x/set", self.set_x)
        contr.addRecive("2d/image/location/y/set", self.set_y)

        self.laserMax = 65
        self.laserMin = 22
        self.laserOff = 13

        self.feedRate = 800
        self.travelRate = 3000
        self.overScan = 3
        self.scanGap = 0.1
        self.resX = 0.1  # gap bettwen pixels
        self.whiteLevel = 253

        horizontalLayout = QVBoxLayout()
        horizontalLayout.addWidget(self.initLaserManipulationSection())
        horizontalLayout.addWidget(self.initSpeedManipulationSection())
        horizontalLayout.addWidget(self.initResolutionManipulationSection())
        horizontalLayout.addStretch(1)
        self.setLayout(horizontalLayout)

    def initLaserManipulationSection(self):
        grid = QGridLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)

        self.initLaserMinFields(grid, 1)
        self.initLaserMaxFields(grid, 2)
        self.initLaserOffFields(grid, 3)
        self.initWhiteLevelFields(grid, 4)

        groupbox = QGroupBox("Power manipulation")
        groupbox.setLayout(grid)
        return groupbox

    def initSpeedManipulationSection(self):
        grid = QGridLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)

        self.initTravelFields(grid, 1)
        self.initFeedFields(grid, 2)

        groupbox = QGroupBox("Rate manipulation")
        groupbox.setLayout(grid)
        return groupbox

    def initResolutionManipulationSection(self):
        grid = QGridLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)

        self.initHorizontalResFields(grid, 1)
        self.initVerticalResFields(grid, 2)
        self.initOverscanFields(grid, 3)

        groupbox = QGroupBox("Resolution manipulation")
        groupbox.setLayout(grid)
        return groupbox

    def initLaserMinFields(self, grid, row):
        grid.addWidget(QLabel("Laser Min Power:"), row, 0)
        int_validate = QIntValidator()
        min_power_input = QLineEdit("22")
        min_power_input.setValidator(int_validate)
        min_power_input.textChanged.connect(self.set_min_laser)
        grid.addWidget(min_power_input, row, 1)
        grid.addWidget(QLabel("[0-255]"), row, 2)

    def initLaserMaxFields(self, grid, row):
        grid.addWidget(QLabel("Laser Max Power:"), row, 0)
        int_validate = QIntValidator()
        max_power_input = QLineEdit("65")
        max_power_input.setValidator(int_validate)
        max_power_input.textChanged.connect(self.set_max_laser)
        grid.addWidget(max_power_input, row, 1)
        grid.addWidget(QLabel("[0-255]"), row, 2)

    def initLaserOffFields(self, grid, row):
        grid.addWidget(QLabel("Laser Off Power:"), row, 0)
        int_validate = QIntValidator()
        off_power_input = QLineEdit("13")
        off_power_input.setValidator(int_validate)
        off_power_input.textChanged.connect(self.set_off_laser)
        grid.addWidget(off_power_input, row, 1)
        grid.addWidget(QLabel("[0-255]"), row, 2)

    def initWhiteLevelFields(self, grid, row):
        grid.addWidget(QLabel("Skip over values above:"), row, 0)
        int_validate = QIntValidator()
        tmp = QLineEdit("253")
        tmp.setValidator(int_validate)
        tmp.textChanged.connect(self.set_whitelevel_laser)
        grid.addWidget(tmp, row, 1)
        grid.addWidget(QLabel("[0-255]"), row, 2)

    def initTravelFields(self, grid, row):
        grid.addWidget(QLabel("Travel (noncutting) Rate:"), row, 0)
        int_validate = QIntValidator()
        tmp = QLineEdit("3000")
        tmp.setValidator(int_validate)
        tmp.textChanged.connect(self.set_travel)
        grid.addWidget(tmp, row, 1)
        grid.addWidget(QLabel("[mm/min]"), row, 2)

    def initFeedFields(self, grid, row):
        grid.addWidget(QLabel("Scan (cutting) Rate:"), row, 0)
        int_validate = QIntValidator()
        tmp = QLineEdit("800")
        tmp.setValidator(int_validate)
        tmp.textChanged.connect(self.set_feed)
        grid.addWidget(tmp, row, 1)
        grid.addWidget(QLabel("[mm/min]"), row, 2)

    def initHorizontalResFields(self, grid, row):
        grid.addWidget(QLabel("Horizontal Resolution:"), row, 0)
        int_validate = QIntValidator()
        tmp = QLineEdit("0.1")
        tmp.setValidator(int_validate)
        tmp.textChanged.connect(self.set_h_res)
        grid.addWidget(tmp, row, 1)
        grid.addWidget(QLabel("[mm/pixel]"), row, 2)

    def initVerticalResFields(self, grid, row):
        grid.addWidget(QLabel("Vertical Resolution:"), row, 0)
        int_validate = QIntValidator()
        tmp = QLineEdit("0.1")
        tmp.setValidator(int_validate)
        tmp.textChanged.connect(self.set_v_res)
        grid.addWidget(tmp, row, 1)
        grid.addWidget(QLabel("[mm/pixel]"), row, 2)

    def initOverscanFields(self, grid, row):
        grid.addWidget(QLabel("Overscan Distance:"), row, 0)
        int_validate = QIntValidator()
        tmp = QLineEdit("3")
        tmp.setValidator(int_validate)
        tmp.textChanged.connect(self.set_overscan)
        grid.addWidget(tmp, row, 1)
        grid.addWidget(QLabel("[mm]"), row, 2)

    # setters
    def set_x(self, value):
        self.x_offset = value

    def set_y(self, value):
        self.y_offset = value

    def set_image(self, image):
        self.image = image
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        self.image.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        self.imagePIL = pil_im
        width, height = self.imagePIL.size
        print(width, '-', height)
        # enhanced_im.save('original-image.png')

    def set_min_laser(self):
        tmp = int(self.sender().text())
        print(tmp)
        if tmp > 255:
            self.laserMin = 255
        elif tmp < 0:
            self.laserMin = 0
        else:
            self.laserMin = tmp

    def set_max_laser(self):
        tmp = int(self.sender().text())
        if tmp > 255:
            self.laserMax = 255
        elif tmp < 0:
            self.laserMax = 0
        else:
            self.laserMax = tmp

    def set_off_laser(self):
        tmp = int(self.sender().text())
        if tmp > 255:
            self.laserOff = 255
        elif tmp < 0:
            self.laserOff = 0
        else:
            self.laserOff = tmp

    def set_whitelevel_laser(self):
        tmp = int(self.sender().text())
        if tmp > 255:
            self.whiteLevel = 255
        elif tmp < 0:
            self.whiteLevel = 0
        else:
            self.whiteLevel = tmp

    def set_travel(self):
        self.travelRate = int(self.sender().text())

    def set_feed(self):
        self.feedRate = int(self.sender().text())

    def set_h_res(self):
        self.resX = int(self.sender().text())

    def set_v_res(self):
        self.scanGap = int(self.sender().text())

    def set_overscan(self):
        self.overScan = int(self.sender().text())

    def bedChanged(self, x, y):
        self._xBed = x
        self._yBed = y

    def process(self):
        img = np.array(self.imagePIL.convert('L'))
        for i in img:
            pass

        w, h = self.imagePIL.size
        offsetY = self.y_offset
        offsetX = self.x_offset

        sizeY = h*self._yBed/550  # in mm
        sizeX = w*self._xBed/550

        pixelsX = round(sizeX / self.resX)
        pixelsY = round(sizeY / self.scanGap)

        # loop through the lines
        lineIndex = 0
        line = offsetY

        prevValue = self.laserOff

        while (line < sizeY + offsetY and lineIndex < h):
            # analyze the row and find first and last nonwhite pixels
            firstX = -1
            # initialize to impossible value
            lastX = -1
            # initialize to impossible value
            pixelIndex = 0
            while (pixelIndex < w):
                value = img[pixelIndex][lineIndex]

                if (value < self.whiteLevel):
                    # If image data (IE nonwhite)
                    if (firstX == -1):
                        # mark this as the first nonwhite pixel
                        firstX = pixelIndex

                    lastX = pixelIndex
                    # Track the last seen nonwhite pixel

                pixelIndex += 1

            # if there are no Nonwhite pixels we can just skip this line altogether
            if (lastX < 0 or firstX < 0):
                self.object_gcode += ";Line " + \
                    str(lineIndex) + " Skipped " + \
                    str(lastX) + " " + str(firstX) + "\n"
                # print(";Line " + str(lineIndex) + " Skipped " +
                #       str(lastX) + " " + str(firstX) + "\n", end="")
                lineIndex += 1
                # Next line GO!
                continue

            pixelIndex = firstX
            # Start at the first nonwhite pixel
            pixel = offsetX + firstX * self.resX
            while (pixel < sizeX + offsetX and pixelIndex < pixelsX):
                # abort the loop early if there are no more nonwhite pixels
                if (pixelIndex == lastX):
                    self.object_gcode += ";Skip The Rest\n"
                    break

                # If this is the first nonwhite pixel we have to move to the correct line, remembering the self.overScan offset
                if (pixelIndex == firstX):
                    self.object_gcode += str(str(str("G1 X" + str(round(pixel - self.overScan, 4))) + " Y") +
                                             str(round(line, 4))) + str(" F" + str(self.travelRate) + "\n")
                    # travel quickly to the line start position
                    self.object_gcode += "G1 F" + str(self.feedRate) + "\n"
                    # Set travel speed to the right speed for etching
                    self.object_gcode += str(str(str("G1 X" + str(round(pixel, 4))) + " Y") +
                                             str(round(line, 4))) + "\n"
                    # Do move
                else:
                    self.object_gcode += str("G1 X" +
                                             str(round(pixel, 4))) + "\n"

                # Continue moving
                value = img[pixelIndex][lineIndex]

                value = round(
                    np.interp(value, [255, 0], [self.laserMin, self.laserMax]), 1)
                if (value != prevValue):
                    # Is the laser power different? no need to send the same power again
                    self.object_gcode += "M106 S" + str(value) + "\n"

                # Write out the laser value
                prevValue = value
                # Save the laser power for the next loop
                pixelIndex += 1
                # Next pixel!
                pixel += self.resX

            self.object_gcode += "M106 S" + str(self.laserOff) + ";\n\n"
            # Turn off the power for the re-trace
            prevValue = self.laserOff
            # Clear out the 'previous value' comparison
            lineIndex += 1
            # Next line!
            line += self.scanGap

    def loadSettings(self):
        settings = Settings()
        dict = settings.listOfPrinterPresets[settings.activePrinterPreset]
        self._xBed = float(dict['bed_size_x'])
        self._yBed = float(dict['bed_size_y'])


class TabContainerWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(350)
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tab1 = ModelManipulation()
        self.tab2 = ImageManipulation()
        self.tab3 = LaserManipulation()
        self.tab4 = GcodeSettings()

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.tabs.addTab(self.tab1, "Model")
        self.tabs.addTab(self.tab2, "Image")
        self.tabs.addTab(self.tab3, "Engraving")
        self.tabs.addTab(self.tab4, "G-code")

        self.layout.addWidget(self.tabs)
        self.processBtn = QPushButton("Process")
        self.processBtn.clicked.connect(self.process)
        self.layout.addWidget(self.processBtn)
        self.exportBtn = QPushButton("Export G-code")
        self.exportBtn.clicked.connect(self.export)
        self.exportBtn.setEnabled(False)
        self.layout.addWidget(self.exportBtn)
        self.setLayout(self.layout)

        self.tab3.loadSettings()

    def process(self):
        self.tab3.process()
        self.exportBtn.setEnabled(True)

    def export(self):
        fname, tmp = QFileDialog.getSaveFileName(
            self, 'Save File', "out.gcode", '*.gcode', '', options=QFileDialog.DontUseNativeDialog)
        #tmp=fname.rsplit('/', 1)
        if fname:
            with open(fname, 'w') as file:
                file.write(self.tab4.gcodeTextEditStart.toPlainText())
                file.write('\n')
                file.write(self.tab3.object_gcode)
                file.write('\n')
                file.write(self.tab4.gcodeTextEditEnd.toPlainText())


class GcodeSettings(QWidget):
    def __init__(self):
        super().__init__()
        horizontalLayout = QVBoxLayout()
        self.setLayout(horizontalLayout)

        settings = Settings()
        horizontalLayout.addWidget(QLabel("Start G-code"))
        self.gcodeTextEditStart = QPlainTextEdit()
        self.gcodeTextEditStart.insertPlainText(settings.gcode["start"])
        horizontalLayout.addWidget(self.gcodeTextEditStart)

        horizontalLayout.addWidget(QLabel("End G-code"))
        self.gcodeTextEditEnd = QPlainTextEdit()
        self.gcodeTextEditEnd.insertPlainText(settings.gcode["end"])
        horizontalLayout.addWidget(self.gcodeTextEditEnd)
