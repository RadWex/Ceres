from PySide2.QtWidgets import (QGridLayout, QVBoxLayout,
                               QLayout, QLabel,
                               QLineEdit, QSlider,
                               QWidget, QHBoxLayout,
                               QGroupBox)
from PySide2.QtGui import QPixmap, QDoubleValidator
from PySide2.QtCore import Qt, Signal, QBuffer
from Controller import Controller
from PIL import ImageEnhance, Image
from PIL.ImageQt import ImageQt
import io


class ImageManipulation(QWidget):
    contrastChangeSig = Signal(int)
    imageChangeSig = Signal(QPixmap)
    xImageLocationChangeSig = Signal(float)
    imageScaleChangeSig = Signal(float)
    yImageLocationChangeSig = Signal(float)
    imageRotateChangeSig = Signal(float)

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addRecive("2d/image/name", self.set_model_name)
        contr.addRecive("2d/image", self.set_image)
        contr.addRecive("2d/image/location/x/set", self.set_x)
        contr.addRecive("2d/image/location/y/set", self.set_y)
        contr.addRecive("2d/image/scale/set", self.set_scale)
        contr.addRecive("2d/image/rotation/set", self.set_rotation)
        contr.addSend("2d/image/off", self.imageChangeSig)
        contr.addSend("2d/image/contrast", self.contrastChangeSig)
        contr.addSend("2d/image/location/x", self.xImageLocationChangeSig)
        contr.addSend("2d/image/location/y", self.yImageLocationChangeSig)
        contr.addSend("2d/image/scale", self.imageScaleChangeSig)
        contr.addSend("2d/image/rotation", self.imageRotateChangeSig)

        self.image = None

        horizontalLayout = QVBoxLayout()
        horizontalLayout.addWidget(self.initImageNameSection())
        horizontalLayout.addWidget(self.initImageManipulationSection())
        horizontalLayout.addWidget(self.initImageSettingsSection())
        horizontalLayout.addStretch(1)
        self.setLayout(horizontalLayout)

    def initImageNameSection(self):
        layout = QHBoxLayout()
        self.name = QLabel()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name)
        groupbox = QGroupBox(self)
        groupbox.setLayout(layout)
        return groupbox

    def initImageManipulationSection(self):
        grid = QGridLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)

        xLabel = QLabel("X")
        xLabel.setAlignment(Qt.AlignCenter)
        grid.addWidget(xLabel, 0, 1)
        yLabel = QLabel("Y")
        yLabel.setAlignment(Qt.AlignCenter)
        grid.addWidget(yLabel, 0, 2)

        self.initLocationFields(grid, 1)
        self.initRotationFields(grid, 2)
        self.initScaleFields(grid, 3)

        groupbox = QGroupBox("Image manipulation")
        groupbox.setLayout(grid)

        return groupbox

    def initLocationFields(self, grid, row):
        grid.addWidget(QLabel("Position:"), row, 0)
        double_validate = QDoubleValidator()
        self.x_input = QLineEdit("0")
        self.x_input.setValidator(double_validate)
        self.x_input.returnPressed.connect(self.send_x)
        grid.addWidget(self.x_input, row, 1)
        self.y_input = QLineEdit("0")
        self.y_input.setValidator(double_validate)
        self.y_input.returnPressed.connect(self.send_y)
        grid.addWidget(self.y_input, row, 2)
        grid.addWidget(QLabel("mm"), row, 3)

    def initRotationFields(self, grid, row):
        grid.addWidget(QLabel("Rotate:"), row, 0)
        double_validate = QDoubleValidator()
        self.x_rot_input = QLineEdit("0")
        self.x_rot_input.setValidator(double_validate)
        self.x_rot_input.returnPressed.connect(self.send_rotation)
        grid.addWidget(self.x_rot_input, row, 1)
        grid.addWidget(QLabel("°"), row, 2)

    def initScaleFields(self, grid, row):
        grid.addWidget(QLabel("Scale factor:"), row, 0)
        double_validate = QDoubleValidator()
        self.x_scale_input = QLineEdit("100")
        self.x_scale_input.setValidator(double_validate)
        self.x_scale_input.returnPressed.connect(self.send_scale)
        grid.addWidget(self.x_scale_input, row, 1)
        grid.addWidget(QLabel("%"), row, 2)

    def initImageSettingsSection(self):
        grid = QGridLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)

        grid.addWidget(QLabel("Brightness: "), 0, 0)
        self.sl2 = QSlider(Qt.Horizontal)
        self.sl2.setMinimum(0)
        self.sl2.setMaximum(40)
        self.sl2.setValue(10)
        self.sl2.valueChanged.connect(self.valuechange2)
        grid.addWidget(self.sl2, 0, 1)

        grid.addWidget(QLabel("Contrast: "), 2, 0)
        self.sl3 = QSlider(Qt.Horizontal)
        self.sl3.setMinimum(0)
        self.sl3.setMaximum(40)
        self.sl3.setValue(10)
        self.sl3.valueChanged.connect(self.contrast_change)
        grid.addWidget(self.sl3, 2, 1)

        groupbox = QGroupBox("Image settings")
        groupbox.setLayout(grid)

        return groupbox

    def set_model_name(self, message):
        self.name.setText(message)

    def set_image(self, image):
        print("image in tab")
        self.image = image
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        self.image.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        self.imagePIL = pil_im

    def valuechange2(self):
        size = self.sl2.value()
        size = size / 10
        enhancer = ImageEnhance.Brightness(self.imagePIL)
        enhanced_im = enhancer.enhance(size)
        img = ImageQt(enhanced_im)
        pixmap = QPixmap.fromImage(img)
        self.imageChangeSig.emit(pixmap)

    def contrast_change(self):
        size = self.sl3.value()
        size = size / 10
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        self.image.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        enhancer = ImageEnhance.Contrast(pil_im)
        enhanced_im = enhancer.enhance(size)
        img = ImageQt(enhanced_im)
        pixmap = QPixmap.fromImage(img)
        self.imageChangeSig.emit(pixmap)

    # getters
    def send_x(self):
        tmp = float(self.sender().text())
        self.xImageLocationChangeSig.emit(tmp)

    def send_y(self):
        tmp = float(self.sender().text())
        self.yImageLocationChangeSig.emit(tmp)

    def send_scale(self):
        tmp = float(self.sender().text())
        self.imageScaleChangeSig.emit(tmp)

    def send_rotation(self):
        tmp = float(self.sender().text())
        self.imageRotateChangeSig.emit(tmp)

    # setters
    def set_x(self, value):
        self.x_input.setText("{:.2f}".format(value))

    def set_y(self, value):
        self.y_input.setText("{:.2f}".format(value))

    def set_scale(self, value):
        self.x_scale_input.setText("{:.2f}".format(value))

    def set_rotation(self, value):
        self.x_rot_input.setText("{:.2f}".format(value))
