from PySide2.QtWidgets import (QGridLayout, QVBoxLayout,
                               QLayout, QLabel,
                               QLineEdit, QSlider,
                               QWidget)
from PySide2.QtGui import QPixmap, QDoubleValidator
from PySide2.QtCore import Qt


class ImageManipulation(QWidget):
    def __init__(self):
        super().__init__()
        #self.imageWidget = ptr_image_widget
        grid = QGridLayout()
        horizontalLayout = QVBoxLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)
        horizontalLayout.addLayout(grid)
        self.setLayout(horizontalLayout)

        self.name = QLabel("Name: tex.jpg")
        horizontalLayout.addWidget(self.name)

        xLabel = QLabel("X")
        # xLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        xLabel.setAlignment(Qt.AlignVCenter)
        grid.addWidget(xLabel, 0, 1)

        grid.addWidget(QLabel("Y"), 0, 2)
        grid.addWidget(QLabel("Position:"), 1, 0)
        grid.addWidget(QLabel("Rotate:"), 2, 0)
        grid.addWidget(QLabel("Scale"), 3, 0)

        double_validate = QDoubleValidator()
        x_input = QLineEdit("0")
        x_input.setValidator(double_validate)
        x_input.returnPressed.connect(self.get_x)
        grid.addWidget(x_input, 1, 1)
        y_input = QLineEdit("0")
        y_input.setValidator(double_validate)
        y_input.returnPressed.connect(self.get_y)
        grid.addWidget(y_input, 1, 2)

        rot_input = QLineEdit("0")
        rot_input.setValidator(double_validate)
        # rot_input.returnPressed.connect(self.rotate)
        grid.addWidget(rot_input, 2, 1)

        x_scale_input = QLineEdit("100")
        x_scale_input.setValidator(double_validate)
        x_scale_input.returnPressed.connect(self.set_scale_x)
        grid.addWidget(x_scale_input, 3, 1)

        grid.addWidget(QLabel("Opacity: "), 4, 0)
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(100)
        self.sl.valueChanged.connect(self.valuechange)
        grid.addWidget(self.sl, 4, 1)

        grid.addWidget(QLabel("Brightness: "), 5, 0)
        self.sl2 = QSlider(Qt.Horizontal)
        self.sl2.setMinimum(0)
        self.sl2.setMaximum(40)
        self.sl2.setValue(10)
        self.sl2.valueChanged.connect(self.valuechange2)
        grid.addWidget(self.sl2, 5, 1)

        grid.addWidget(QLabel("Contrast: "), 6, 0)
        self.sl3 = QSlider(Qt.Horizontal)
        self.sl3.setMinimum(0)
        self.sl3.setMaximum(40)
        self.sl3.setValue(10)
        self.sl3.valueChanged.connect(self.valuechange3)
        grid.addWidget(self.sl3, 6, 1)
        # xLabel = QLabel("X")

        xLabel.setAlignment(Qt.AlignVCenter)
        horizontalLayout.addStretch(1)

    def valuechange(self):
        size = self.sl.value()
        size = size / 100
        self.imageWidget.item1.setOpacity(size)

    def valuechange2(self):
        size = self.sl2.value()
        size = size / 10
        global im
        enhancer = ImageEnhance.Brightness(im)
        enhanced_im = enhancer.enhance(size)
        img = ImageQt(enhanced_im)
        pixmap02 = QPixmap.fromImage(img)
        self.imageWidget.item1.setPixmap(pixmap02)

    def valuechange3(self):
        size = self.sl3.value()
        size = size / 10
        global im
        enhancer = ImageEnhance.Contrast(im)
        enhanced_im = enhancer.enhance(size)
        img = ImageQt(enhanced_im)
        pixmap02 = QPixmap.fromImage(img)
        self.imageWidget.item1.setPixmap(pixmap02)

    def get_x(self):
        # print(self.sender().text())
        tmp = float(self.sender().text())
        tmp = tmp*450/200
        self.imageWidget.item1.setX(tmp)
        # self.imageWidget.item1.scale(1, -1)

    def get_y(self):
        #self.imageWidget.item1.setTransform(QTransform.fromScale(1, -1))
        tmp = float(self.sender().text())
        tmp = tmp*450/200
        self.imageWidget.item1.setY(-tmp-256)

    def set_scale_x(self):
        tmp = int(self.sender().text())/100
        self.imageWidget.item1.setScale(tmp)
