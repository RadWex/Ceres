from PySide2.QtWidgets import (QWidget, QGridLayout,
                               QGroupBox, QVBoxLayout,
                               QLayout, QLabel,
                               QLineEdit, QHBoxLayout)
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

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addRecive("3d/model/name", self.set_model_name)
        contr.addRecive("3d/model/tris", self.set_model_count)
        contr.addRecive("3d/model/dimension", self.set_model_dimension)
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

    def initLocationFields(self, grid, row):
        grid.addWidget(QLabel("Position:"), row, 0)
        double_validate = QDoubleValidator()
        x_input = QLineEdit("0")
        x_input.setValidator(double_validate)
        x_input.returnPressed.connect(self.get_x)
        grid.addWidget(x_input, row, 1)
        y_input = QLineEdit("0")
        y_input.setValidator(double_validate)
        y_input.returnPressed.connect(self.get_y)
        grid.addWidget(y_input, row, 2)
        z_input = QLineEdit("0")
        z_input.setValidator(double_validate)
        z_input.returnPressed.connect(self.get_z)
        grid.addWidget(z_input, row, 3)
        grid.addWidget(QLabel("mm"), row, 4)

    def initRotationFields(self, grid, row):
        grid.addWidget(QLabel("Rotate:"), row, 0)
        double_validate = QDoubleValidator()
        x_rot_input = QLineEdit("0")
        x_rot_input.setValidator(double_validate)
        x_rot_input.returnPressed.connect(self.set_rot_x)
        grid.addWidget(x_rot_input, row, 1)
        y_rot_input = QLineEdit("0")
        y_rot_input.setValidator(double_validate)
        y_rot_input.returnPressed.connect(self.set_rot_y)
        grid.addWidget(y_rot_input, row, 2)
        z_rot_input = QLineEdit("0")
        z_rot_input.setValidator(double_validate)
        z_rot_input.returnPressed.connect(self.set_rot_z)
        grid.addWidget(z_rot_input, row, 3)
        grid.addWidget(QLabel("°"), row, 4)

    def initScaleFields(self, grid, row):
        grid.addWidget(QLabel("Scale factors:"), row, 0)
        double_validate = QDoubleValidator()
        x_scale_input = QLineEdit("100")
        x_scale_input.setValidator(double_validate)
        x_scale_input.returnPressed.connect(self.set_scale_x)
        grid.addWidget(x_scale_input, row, 1)
        y_scale_input = QLineEdit("100")
        y_scale_input.setValidator(double_validate)
        y_scale_input.returnPressed.connect(self.set_scale_y)
        grid.addWidget(y_scale_input, row, 2)
        z_scale_input = QLineEdit("100")
        z_scale_input.setValidator(double_validate)
        z_scale_input.returnPressed.connect(self.set_scale_z)
        grid.addWidget(z_scale_input, row, 3)
        grid.addWidget(QLabel("%"), row, 4)

    def initDimensionFields(self, grid, row):
        double_validate = QDoubleValidator()
        grid.addWidget(QLabel("Size:"), row, 0)
        x_demension_input = QLineEdit("0")
        x_demension_input.setValidator(double_validate)
        grid.addWidget(x_demension_input, row, 1)
        y_demension_input = QLineEdit("0")
        y_demension_input.setValidator(double_validate)
        grid.addWidget(y_demension_input, row, 2)
        z_demension_input = QLineEdit("0")
        z_demension_input.setValidator(double_validate)
        grid.addWidget(z_demension_input, 4, 3)
        grid.addWidget(QLabel("mm"), row, 4)

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
        xLabel.setAlignment(Qt.AlignVCenter)
        grid.addWidget(xLabel, 0, 1)

        grid.addWidget(QLabel("Y"), 0, 2)
        grid.addWidget(QLabel("Z"), 0, 3)

        self.initLocationFields(grid, 1)
        self.initRotationFields(grid, 2)
        self.initScaleFields(grid, 3)
        self.initDimensionFields(grid, 4)

        groupbox = QGroupBox("Object manipulation")
        groupbox.setLayout(grid)

        return groupbox

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

    def set_model_name(self, message):
        self.name.setText(message)

    def set_model_count(self, tris):
        self.infoTris.setText(str(tris))

    def set_model_dimension(self, x, y, z):
        self.infoDimension.setText(str(x)+"x"+str(y)+"x"+str(z))

    def get_x(self):
        self.xLocationChangeSig.emit(float(self.sender().text()))

    def get_y(self):
        self.yLocationChangeSig.emit(float(self.sender().text()))

    def get_z(self):
        self.zLocationChangeSig.emit(float(self.sender().text()))

    def set_rot_x(self):
        self.xRotationChangeSig.emit(float(self.sender().text()))

    def set_rot_y(self):
        self.yRotationChangeSig.emit(float(self.sender().text()))

    def set_rot_z(self):
        self.zRotationChangeSig.emit(float(self.sender().text()))

    def set_scale_x(self):
        self.xScaleChangeSig.emit(float(self.sender().text()))

    def set_scale_y(self):
        self.yScaleChangeSig.emit(float(self.sender().text()))

    def set_scale_z(self):
        self.zScaleChangeSig.emit(float(self.sender().text()))
