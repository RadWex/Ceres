from PySide2.QtWidgets import (QWidget, QGridLayout,
                               QGroupBox, QVBoxLayout,
                               QLayout, QLabel,
                               QLineEdit)
from PySide2.QtGui import QDoubleValidator
from PySide2.QtCore import Qt

provider = None


class ModelManipulation(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        groupbox_name = QGroupBox(self)
        horizontalLayout = QVBoxLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)
        horizontalLayout.addWidget(groupbox_name)
        horizontalLayout_for_groupbox = QVBoxLayout()
        groupbox_name.setLayout(horizontalLayout_for_groupbox)
        self.name = QLabel("Name:")
        horizontalLayout_for_groupbox.addWidget(self.name)
        horizontalLayout.addLayout(grid)
        self.setLayout(horizontalLayout)
        xLabel = QLabel("X")
        # xLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        xLabel.setAlignment(Qt.AlignVCenter)
        grid.addWidget(xLabel, 0, 1)

        grid.addWidget(QLabel("Y"), 0, 2)
        grid.addWidget(QLabel("Z"), 0, 3)
        grid.addWidget(QLabel("Position:"), 1, 0)
        grid.addWidget(QLabel("Rotate:"), 2, 0)
        grid.addWidget(QLabel("Scale factors:"), 3, 0)
        grid.addWidget(QLabel("Size:"), 4, 0)
        double_validate = QDoubleValidator()

        x_input = QLineEdit("0")
        x_input.setValidator(double_validate)
        x_input.returnPressed.connect(self.get_x)
        grid.addWidget(x_input, 1, 1)
        y_input = QLineEdit("0")
        y_input.setValidator(double_validate)
        y_input.returnPressed.connect(self.get_y)
        grid.addWidget(y_input, 1, 2)
        z_input = QLineEdit("0")
        z_input.setValidator(double_validate)
        z_input.returnPressed.connect(self.get_z)
        grid.addWidget(z_input, 1, 3)

        x_rot_input = QLineEdit("0")
        x_rot_input.setValidator(double_validate)
        x_rot_input.returnPressed.connect(self.set_rot_x)
        grid.addWidget(x_rot_input, 2, 1)
        y_rot_input = QLineEdit("0")
        y_rot_input.setValidator(double_validate)
        y_rot_input.returnPressed.connect(self.set_rot_y)
        grid.addWidget(y_rot_input, 2, 2)
        z_rot_input = QLineEdit("0")
        z_rot_input.setValidator(double_validate)
        z_rot_input.returnPressed.connect(self.set_rot_z)
        grid.addWidget(z_rot_input, 2, 3)

        x_scale_input = QLineEdit("100")
        x_scale_input.setValidator(double_validate)
        x_scale_input.returnPressed.connect(self.set_scale_x)
        grid.addWidget(x_scale_input, 3, 1)
        y_scale_input = QLineEdit("100")
        y_scale_input.setValidator(double_validate)
        y_scale_input.returnPressed.connect(self.set_scale_y)
        grid.addWidget(y_scale_input, 3, 2)
        z_scale_input = QLineEdit("100")
        z_scale_input.setValidator(double_validate)
        z_scale_input.returnPressed.connect(self.set_scale_z)
        grid.addWidget(z_scale_input, 3, 3)

        x_demension_input = QLineEdit("0")
        x_demension_input.setValidator(double_validate)
        grid.addWidget(x_demension_input, 4, 1)
        y_demension_input = QLineEdit("0")
        y_demension_input.setValidator(double_validate)
        grid.addWidget(y_demension_input, 4, 2)
        z_demension_input = QLineEdit("0")
        z_demension_input.setValidator(double_validate)
        grid.addWidget(z_demension_input, 4, 3)

        grid.addWidget(QLabel("mm"), 1, 4)
        grid.addWidget(QLabel("°"), 2, 4)
        grid.addWidget(QLabel("%"), 3, 4)
        grid.addWidget(QLabel("mm"), 4, 4)

        horizontalLayout.addStretch(1)

    def get_x(self):
        # print(self.sender().text())
        global provider
        provider.x = float(self.sender().text())

    def get_y(self):
        global provider
        provider.y = float(self.sender().text())

    def get_z(self):
        global provider
        provider.z = float(self.sender().text())

    def set_rot_x(self):
        global provider
        provider.x_rot = float(self.sender().text())

    def set_rot_y(self):
        global provider
        provider.y_rot = float(self.sender().text())

    def set_rot_z(self):
        global provider
        provider.z_rot = float(self.sender().text())

    def set_scale_x(self):
        global provider
        provider.x_scale = float(self.sender().text())

    def set_scale_y(self):
        global provider
        provider.y_scale = float(self.sender().text())

    def set_scale_z(self):
        global provider
        provider.z_scale = float(self.sender().text())
