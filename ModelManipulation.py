from PySide2.QtWidgets import (QWidget, QGridLayout,
                               QGroupBox, QVBoxLayout,
                               QLayout, QLabel,
                               QLineEdit, QHBoxLayout,
                               QSizePolicy)
from PySide2.QtGui import QDoubleValidator
from PySide2.QtCore import Qt, Signal
from Controller import Controller

provider = None


class ModelManipulation(QWidget):
    xLocationChangeSig = Signal(float)
    yLocationChangeSig = Signal(float)
    zLocationChangeSig = Signal(float)
    xRotationChangeSig = Signal(float)
    yRotationChangeSig = Signal(float)
    zRotationChangeSig = Signal(float)
    xScaleChangeSig = Signal(float)
    yScaleChangeSig = Signal(float)
    zScaleChangeSig = Signal(float)
    origin = [0, 0, 0]
    dimension = [1, 1, 1]

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addRecive("3d/model/name", self.set_model_name)
        contr.addRecive("3d/model/tris", self.set_model_count)
        contr.addRecive("3d/model/dimension", self.set_model_dimension)
        contr.addRecive("3d/model/origin", self.set_origin)

        contr.addRecive("3d/model/location/x/set", self.set_x)
        contr.addRecive("3d/model/location/y/set", self.set_y)
        contr.addRecive("3d/model/location/z/set", self.set_z)
        contr.addRecive("3d/model/rotation/x/set", self.set_rot_x)
        contr.addRecive("3d/model/rotation/y/set", self.set_rot_y)
        contr.addRecive("3d/model/rotation/z/set", self.set_rot_z)
        contr.addRecive("3d/model/scale/x", self.set_scale_x)
        contr.addRecive("3d/model/scale/y", self.set_scale_y)
        contr.addRecive("3d/model/scale/z", self.set_scale_z)

        contr.addSend("3d/model/location/x", self.xLocationChangeSig)
        contr.addSend("3d/model/location/y", self.yLocationChangeSig)
        contr.addSend("3d/model/location/z", self.zLocationChangeSig)
        contr.addSend("3d/model/rotation/x", self.xRotationChangeSig)
        contr.addSend("3d/model/rotation/y", self.yRotationChangeSig)
        contr.addSend("3d/model/rotation/z", self.zRotationChangeSig)
        contr.addSend("3d/model/scale/x", self.xScaleChangeSig)
        contr.addSend("3d/model/scale/y", self.yScaleChangeSig)
        contr.addSend("3d/model/scale/z", self.zScaleChangeSig)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.initModelNameSection())
        mainLayout.addWidget(self.initModelManipulationSection())
        mainLayout.addWidget(self.initModelInfoSection())
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    def initModelNameSection(self):
        layout = QHBoxLayout()
        self.name = QLabel()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name)
        groupbox = QGroupBox(self)
        groupbox.setLayout(layout)
        return groupbox

    def initModelManipulationSection(self):
        grid = QGridLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)

        xLabel = QLabel("X")
        xLabel.setAlignment(Qt.AlignCenter)
        grid.addWidget(xLabel, 0, 1)

        yLabel = QLabel("Y")
        yLabel.setAlignment(Qt.AlignCenter)
        grid.addWidget(yLabel, 0, 2)

        zLabel = QLabel("Z")
        zLabel.setAlignment(Qt.AlignCenter)
        grid.addWidget(zLabel, 0, 3)

        self.initLocationFields(grid, 1)
        self.initRotationFields(grid, 2)
        self.initScaleFields(grid, 3)
        self.initDimensionFields(grid, 4)

        groupbox = QGroupBox("Object manipulation")
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
        self.z_input = QLineEdit("0")
        self.z_input.setValidator(double_validate)
        self.z_input.returnPressed.connect(self.send_z)
        grid.addWidget(self.z_input, row, 3)
        grid.addWidget(QLabel("mm"), row, 4)

    def initRotationFields(self, grid, row):
        grid.addWidget(QLabel("Rotate:"), row, 0)
        double_validate = QDoubleValidator()
        self.x_rot_input = QLineEdit("0")
        self.x_rot_input.setValidator(double_validate)
        self.x_rot_input.returnPressed.connect(self.send_rot_x)
        grid.addWidget(self.x_rot_input, row, 1)
        self.y_rot_input = QLineEdit("0")
        self.y_rot_input.setValidator(double_validate)
        self.y_rot_input.returnPressed.connect(self.send_rot_y)
        grid.addWidget(self.y_rot_input, row, 2)
        self.z_rot_input = QLineEdit("0")
        self.z_rot_input.setValidator(double_validate)
        self.z_rot_input.returnPressed.connect(self.send_rot_z)
        grid.addWidget(self.z_rot_input, row, 3)
        grid.addWidget(QLabel("°"), row, 4)

    def initScaleFields(self, grid, row):
        grid.addWidget(QLabel("Scale factors:"), row, 0)
        double_validate = QDoubleValidator()
        self.x_scale_input = QLineEdit("100")
        self.x_scale_input.setValidator(double_validate)
        self.x_scale_input.returnPressed.connect(self.send_scale_x)
        grid.addWidget(self.x_scale_input, row, 1)
        self.y_scale_input = QLineEdit("100")
        self.y_scale_input.setValidator(double_validate)
        self.y_scale_input.returnPressed.connect(self.send_scale_y)
        grid.addWidget(self.y_scale_input, row, 2)
        self.z_scale_input = QLineEdit("100")
        self.z_scale_input.setValidator(double_validate)
        self.z_scale_input.returnPressed.connect(self.send_scale_z)
        grid.addWidget(self.z_scale_input, row, 3)
        grid.addWidget(QLabel("%"), row, 4)

    def initDimensionFields(self, grid, row):
        double_validate = QDoubleValidator()
        grid.addWidget(QLabel("Size:"), row, 0)
        self.x_demension_input = QLineEdit("0")
        self.x_demension_input.setValidator(double_validate)
        self.x_demension_input.returnPressed.connect(self.send_dimension_x)
        grid.addWidget(self.x_demension_input, row, 1)
        self.y_demension_input = QLineEdit("0")
        self.y_demension_input.setValidator(double_validate)
        self.y_demension_input.returnPressed.connect(self.send_dimension_y)
        grid.addWidget(self.y_demension_input, row, 2)
        self.z_demension_input = QLineEdit("0")
        self.z_demension_input.setValidator(double_validate)
        self.z_demension_input.returnPressed.connect(self.send_dimension_z)
        grid.addWidget(self.z_demension_input, 4, 3)
        grid.addWidget(QLabel("mm"), row, 4)

    def initModelInfoSection(self):
        grid = QGridLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)
        grid.addWidget(QLabel("Size:"), 0, 0)
        self.infoDimension = QLabel()
        grid.addWidget(self.infoDimension, 0, 1)

        grid.addWidget(QLabel("Tris:"), 1, 0)
        self.infoTris = QLabel()
        grid.addWidget(self.infoTris, 1, 1)

        groupbox = QGroupBox("Info")
        groupbox.setLayout(grid)

        return groupbox

    # set const functions
    def set_model_name(self, message):
        self.name.setText(message)

    def set_model_count(self, tris):
        self.infoTris.setText(str(tris))

    def set_model_dimension(self, x, y, z):
        text = "%.2f x %.2f x %.2f" % (x, y, z)
        self.dimension = [x, y, z]
        self.infoDimension.setText(text)
        self.x_demension_input.setText(str(round(x, 2)))
        self.y_demension_input.setText(str(round(y, 2)))
        self.z_demension_input.setText(str(round(z, 2)))

    def set_origin(self, values):
        self.origin = values

    # send functions
    def send_x(self):
        self.xLocationChangeSig.emit(
            float(self.sender().text())-self.origin[0])

    def send_y(self):
        self.yLocationChangeSig.emit(
            float(self.sender().text())-self.origin[1])

    def send_z(self):
        self.zLocationChangeSig.emit(
            float(self.sender().text())-self.origin[2])

    def send_rot_x(self):
        self.xRotationChangeSig.emit(float(self.sender().text()))

    def send_rot_y(self):
        self.yRotationChangeSig.emit(float(self.sender().text()))

    def send_rot_z(self):
        self.zRotationChangeSig.emit(float(self.sender().text()))

    def send_scale_x(self):
        new_scale = float(self.sender().text())
        self.xScaleChangeSig.emit(new_scale)

    def send_scale_y(self):
        self.yScaleChangeSig.emit(float(self.sender().text()))

    def send_scale_z(self):
        self.zScaleChangeSig.emit(float(self.sender().text()))

    def send_dimension_x(self):
        actual = float(self.x_demension_input.text())
        new = actual/self.dimension[0] * 100
        self.xScaleChangeSig.emit(new)

    def send_dimension_y(self):
        actual = float(self.y_demension_input.text())
        new = actual/self.dimension[1] * 100
        self.yScaleChangeSig.emit(new)

    def send_dimension_z(self):
        actual = float(self.z_demension_input.text())
        new = actual/self.dimension[2] * 100
        self.zScaleChangeSig.emit(new)

    # set functions
    def set_x(self, value):
        tmp = value + self.origin[0]
        self.x_input.setText("{:.2f}".format(tmp))

    def set_y(self, value):
        tmp = value + self.origin[1]
        self.y_input.setText("{:.2f}".format(tmp))

    def set_z(self, value):
        tmp = value + self.origin[2]
        self.z_input.setText("{:.2f}".format(tmp))

    def set_rot_x(self, value):
        self.x_rot_input.setText("{:.2f}".format(value))

    def set_rot_y(self, value):
        self.y_rot_input.setText("{:.2f}".format(value))

    def set_rot_z(self, value):
        self.z_rot_input.setText("{:.2f}".format(value))

    def set_scale_x(self, value):
        self.x_scale_input.setText("{:.2f}".format(value))
        new_dimension = (self.dimension[0] * (value/100))
        self.x_demension_input.setText("{:.2f}".format(new_dimension))

    def set_scale_y(self, value):
        self.y_scale_input.setText("{:.2f}".format(value))
        new_dimension = (self.dimension[1] * (value/100))
        self.y_demension_input.setText("{:.2f}".format(new_dimension))

    def set_scale_z(self, value):
        self.z_scale_input.setText("{:.2f}".format(value))
        new_dimension = (self.dimension[2] * (value/100))
        self.z_demension_input.setText("{:.2f}".format(new_dimension))
