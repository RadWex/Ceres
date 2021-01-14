# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtWidgets import QMainWindow, QApplication, QGridLayout
from PySide2.QtGui import *
from PySide2.QtQuickWidgets import QQuickWidget
# from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, Property, QObject, Slot, QTimer, Signal, Qt
from PySide2.QtWidgets import *
from Settings import Settings

settings = Settings()

class MeshManager(QObject):
    modelChanged = Signal(str)
    xChanged = Signal(float)
    yChanged = Signal(float)
    zChanged = Signal(float)
    x_rot_Changed = Signal(float)
    y_rot_Changed = Signal(float)
    z_rot_Changed = Signal(float)
    x_scale_Changed = Signal(float)
    y_scale_Changed = Signal(float)
    z_scale_Changed = Signal(float)
    def __init__(self, parent=None):
        super(MeshManager, self).__init__(parent)
        self.modelName = ""
        self._x = 0
        self._y = 0
        self._z = 0
        self._x_rot = 0
        self._y_rot = 0
        self._z_rot = 0
        self._x_scale = 1
        self._y_scale = 1
        self._z_scale = 1
        self._modelChange = "meshes/circle.stl"

    @Property(float, notify=xChanged)
    def x(self):
        return self._x

    @x.setter
    def x(self, new_w):
        if self._x != new_w:
            self._x = new_w
            self.xChanged.emit(new_w)

    @Property(float, notify=yChanged)
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        if self._y != new_y:
            self._y = new_y
            self.yChanged.emit(new_y)

    @Property(float, notify=zChanged)
    def z(self):
        return self._z

    @z.setter
    def z(self, new_z):
        if self._z != new_z:
            self._z = new_z
            self.zChanged.emit(new_z)

    @Property(float, notify=x_rot_Changed)
    def x_rot(self):
        return self._x_rot

    @x_rot.setter
    def x_rot(self, angle):
        if self._x_rot != angle:
            self._x_rot = angle
            self.x_rot_Changed.emit(angle)

    @Property(float, notify=y_rot_Changed)
    def y_rot(self):
        return self._y_rot

    @y_rot.setter
    def y_rot(self, angle):
        if self._y_rot != angle:
            self._y_rot = angle
            self.y_rot_Changed.emit(angle)

    @Property(float, notify=z_rot_Changed)
    def z_rot(self):
        return self._z_rot

    @z_rot.setter
    def z_rot(self, angle):
        if self._z_rot != angle:
            self._z_rot = angle
            self.z_rot_Changed.emit(angle)

    @Property(float, notify=x_scale_Changed)
    def x_scale(self):
        return self._x_scale

    @x_scale.setter
    def x_scale(self, angle):
        angle = angle/100.0
        if self._x_scale != angle:
            self._x_scale = angle
            self.x_scale_Changed.emit(angle)

    @Property(float, notify=y_scale_Changed)
    def y_scale(self):
        return self._y_scale

    @y_scale.setter
    def y_scale(self, angle):
        angle = angle/100.0
        if self._y_scale != angle:
            self._y_scale = angle
            self.y_scale_Changed.emit(angle)

    @Property(float, notify=z_scale_Changed)
    def z_scale(self):
        return self._z_scale

    @z_scale.setter
    def z_scale(self, angle):
        angle = angle/100.0
        if self._z_scale != angle:
            self._z_scale = angle
            self.z_scale_Changed.emit(angle)

    @Property(str, notify=modelChanged)
    def modelChange(self):
        return self._modelChange

    @modelChange.setter
    def modelChange(self, path):
        if self._modelChange != path:
            self._modelChange = path
            self.modelChanged.emit(path)


provider = MeshManager()

class GcodeSettings(QWidget):
    def __init__(self):
        super().__init__()
        horizontalLayout = QVBoxLayout()
        self.setLayout(horizontalLayout)

        horizontalLayout.addWidget(QLabel("Start G-code"))
        gcodeTextEditStart = QPlainTextEdit()
        gcodeTextEditStart.insertPlainText(settings.gcode["start"])
        horizontalLayout.addWidget(gcodeTextEditStart)

        horizontalLayout.addWidget(QLabel("End G-code"))
        gcodeTextEditEnd = QPlainTextEdit()
        gcodeTextEditEnd.insertPlainText(settings.gcode["end"])
        horizontalLayout.addWidget(gcodeTextEditEnd)

class ModelManipulation(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        horizontalLayout = QVBoxLayout()
        grid.setSizeConstraint(QLayout.SetMinimumSize)
        self.name = QLabel("Name:")
        horizontalLayout.addWidget(self.name)
        horizontalLayout.addLayout(grid)
        self.setLayout(horizontalLayout)
        xLabel = QLabel("X")
        #xLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        xLabel.setAlignment(Qt.AlignVCenter)
        grid.addWidget(xLabel,0,1)

        grid.addWidget(QLabel("Y"),0,2)
        grid.addWidget(QLabel("Z"),0,3)
        grid.addWidget(QLabel("Position:"),1,0)
        grid.addWidget(QLabel("Rotate:"),2,0)
        grid.addWidget(QLabel("Scale factors:"),3,0)
        grid.addWidget(QLabel("Size:"),4,0)
        double_validate = QDoubleValidator()

        x_input = QLineEdit("0")
        x_input.setValidator(double_validate)
        x_input.returnPressed.connect(self.get_x)
        grid.addWidget(x_input,1,1)
        y_input = QLineEdit("0")
        y_input.setValidator(double_validate)
        y_input.returnPressed.connect(self.get_y)
        grid.addWidget(y_input,1,2)
        z_input = QLineEdit("0")
        z_input.setValidator(double_validate)
        z_input.returnPressed.connect(self.get_z)
        grid.addWidget(z_input,1,3)

        x_rot_input = QLineEdit("0")
        x_rot_input.setValidator(double_validate)
        x_rot_input.returnPressed.connect(self.set_rot_x)
        grid.addWidget(x_rot_input,2,1)
        y_rot_input = QLineEdit("0")
        y_rot_input.setValidator(double_validate)
        y_rot_input.returnPressed.connect(self.set_rot_y)
        grid.addWidget(y_rot_input,2,2)
        z_rot_input = QLineEdit("0")
        z_rot_input.setValidator(double_validate)
        z_rot_input.returnPressed.connect(self.set_rot_z)
        grid.addWidget(z_rot_input,2,3)

        x_scale_input = QLineEdit("100")
        x_scale_input.setValidator(double_validate)
        x_scale_input.returnPressed.connect(self.set_scale_x)
        grid.addWidget(x_scale_input,3,1)
        y_scale_input = QLineEdit("100")
        y_scale_input.setValidator(double_validate)
        y_scale_input.returnPressed.connect(self.set_scale_y)
        grid.addWidget(y_scale_input,3,2)
        z_scale_input = QLineEdit("100")
        z_scale_input.setValidator(double_validate)
        z_scale_input.returnPressed.connect(self.set_scale_z)
        grid.addWidget(z_scale_input,3,3)

        x_demension_input = QLineEdit("0")
        x_demension_input.setValidator(double_validate)
        grid.addWidget(x_demension_input,4,1)
        y_demension_input = QLineEdit("0")
        y_demension_input.setValidator(double_validate)
        grid.addWidget(y_demension_input,4,2)
        z_demension_input = QLineEdit("0")
        z_demension_input.setValidator(double_validate)
        grid.addWidget(z_demension_input,4,3)

        grid.addWidget(QLabel("mm"), 1, 4)
        grid.addWidget(QLabel("°"), 2, 4)
        grid.addWidget(QLabel("%"), 3, 4)
        grid.addWidget(QLabel("mm"), 4, 4)

        horizontalLayout.addStretch(1)

    def get_x(self):
        #print(self.sender().text())
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

class MyTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(350)
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tab1 = ModelManipulation()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = GcodeSettings()

        self.layout.setContentsMargins(0,0,0,0)
        self.tabs.addTab(self.tab1,"Model")
        self.tabs.addTab(self.tab2,"Image")
        self.tabs.addTab(self.tab3,"Engraving")
        self.tabs.addTab(self.tab4,"G-code")

        self.layout.addWidget(self.tabs)
        self.processBtn = QPushButton("Process")
        self.layout.addWidget(self.processBtn)
        self.exportBtn = QPushButton("Export G-code")
        self.exportBtn.clicked.connect(self.get_y)
        self.exportBtn.setEnabled(False)
        self.layout.addWidget(self.exportBtn)
        self.setLayout(self.layout)

    def get_y(self):
        global provider
        provider.modelChange = ""


ref_to_img_widget = None

class Test(QObject):
    def __init__(self):
        super(Test, self).__init__()

    @Slot(QImage)
    def model(self, reply):
        print('from QML: %s' % (reply))
        print('wywolano')
        image = QPixmap.fromImage(reply)
        global ref_to_img_widget
        ref_to_img_widget.addPixmap(image)
        ref_to_img_widget.update()

pyobject = Test()

class Viewer3d(QQuickWidget):
    def __init__(self):
        super().__init__()
        global provider
        self.engine().rootContext().setContextProperty("_renderCaptureProvider", pyobject)
        self.engine().rootContext().setContextProperty("r_manager", provider)
        self.setSource(QUrl.fromLocalFile("main.qml"))
        self.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class ImageWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self._zoom = 0
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        img = QImage(600,500, QImage.Format_ARGB32)
        img.fill(QColor("blue").rgba())
        pixmap01 = QPixmap.fromImage(img)
        self.scene = QGraphicsScene()
        global ref_to_img_widget
        ref_to_img_widget = self.scene
        self.scene.addPixmap(pixmap01)
        img = QImage(50,50, QImage.Format_ARGB32)
        img.fill(QColor("red").rgba())
        pixmap02 = QPixmap.fromImage(img)
        self.item1 = self.scene.addPixmap(pixmap02)
        self.item1.setPos(300,300)
        self.item1.setZValue(1)
        self.setScene(self.scene)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        #if self._zoom > 0:
        self.scale(factor, factor)
        #elif self._zoom == 0:
        #    self.fitInView()
        #else:
        #    self._zoom = 0



class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        view = Viewer3d()
        tab = MyTableWidget()

        image_viewer = ImageWidget()
        layout = QHBoxLayout()
        layout.addWidget(image_viewer)
        layout.addWidget(view)
        layout.addWidget(tab)
        self.setLayout(layout)


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        con = settings.printerSettings
        grid = QGridLayout()
        self.setLayout(grid)
        double_validator = QDoubleValidator()
        grid.addWidget(QLabel("Size:"), 0, 0)
        grid.addWidget(QLabel("x:"), 0, 2)
        bedSizeX = QLineEdit(con['bed_size_x'])
        bedSizeX.setValidator(double_validator)
        #bedSizeX.returnPressed.connect(self.set_rot_x)
        grid.addWidget(bedSizeX,0,3)

        grid.addWidget(QLabel("y:"), 1, 2)
        bedSizeY = QLineEdit(con['bed_size_y'])
        bedSizeY.setValidator(double_validator)
        #bedSizeX.returnPressed.connect(self.set_rot_x)
        grid.addWidget(bedSizeY, 1, 3)

        grid.addWidget(QLabel("Origin:"), 2, 0)
        grid.addWidget(QLabel("x:"), 2, 2)
        originX = QLineEdit(con['origin_x'])
        originX.setValidator(double_validator)
        #bedSizeX.returnPressed.connect(self.set_rot_x)
        grid.addWidget(originX, 2, 3)

        grid.addWidget(QLabel("y:"), 3, 2)
        originY = QLineEdit(con['origin_y'])
        originY.setValidator(double_validator)
        #bedSizeX.returnPressed.connect(self.set_rot_x)
        grid.addWidget(originY, 3, 3)





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        mainWidget = MainWidget()
        self.setCentralWidget(mainWidget)
        self.initialize_menu_bar()
        self.initialize_tool_bar()
        self.setWindowTitle("Ceres")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Zaladowano")

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
        file_menu.addAction(exitAction)
        file_menu.addAction(fileOpenAction)

    def initialize_tool_bar(self):
        tool_menu = QToolBar()
        self.addToolBar(tool_menu)
        action = QAction(QIcon("icons/move.png"),"Move",self)
        action.setIcon(QIcon("icons/move.png"))
        tool_menu.addAction(action)


    def getfile(self):
       fname, tmp = QFileDialog.getOpenFileName(self, 'Open file',
          'c:\\',"Model files (*.obj *.stl *.ply)")
       print(fname)
       global provider
       provider.modelChange = "file:///"+fname
       provider.modelName = fname

    def openSettingsWindow(self):
        self.sw.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    provider.x = 10
    provider.x = 0

    sys.exit(app.exec_())
