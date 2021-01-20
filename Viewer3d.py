import numpy as np
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtCore import Signal, Property, Slot, QUrl, QObject
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtWidgets import QSizePolicy
from PySide2.Qt3DRender import (Qt3DRender)
from Settings import Settings


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


class Window3dManager(QObject):
    xBedChanged = Signal(int)
    yBedChanged = Signal(int)

    def __init__(self, parent=None):
        super(Window3dManager, self).__init__(parent)
        self._xBed = 235
        self._yBed = 235
        self.loadSettings()

    def loadSettings(self):
        settings = Settings()
        self._xBed = settings.printerSettings['bed_size_x']
        self._yBed = settings.printerSettings['bed_size_x']

    @Property(int, notify=xBedChanged)
    def xBed(self):
        return self._xBed

    @xBed.setter
    def xBed(self, new_x):
        if self._xBed != new_x:
            self._xBed = new_x
            self.xBedChanged.emit(new_x)

    @Property(int, notify=yBedChanged)
    def yBed(self):
        return self._yBed

    @yBed.setter
    def yBed(self, new_y):
        if self._yBed != new_y:
            self._yBed = new_y
            self.yBedChanged.emit(new_y)


windowProvider = Window3dManager()


class Test(QObject):
    def __init__(self):
        super(Test, self).__init__()

    @ Slot(Qt3DRender.QGeometry)
    def dawaj_model(self, reply):
        vertexPosition = None
        atributes = reply.attributes()
        for i in atributes:
            if i.name() == 'vertexPosition':
                vertexPosition = i

        vertices_count = vertexPosition.count()
        tmp = np.frombuffer(vertexPosition.buffer().data(), dtype=np.float32)
        arr = np.empty((0, 3), dtype=np.float32)
        iterator = 1
        for i, j, k in zip(tmp[0::3], tmp[1::3], tmp[2::3]):
            if(iterator % 2):
                arr = np.append(arr, np.array(
                    [[i, j, k]], dtype=np.float32), axis=0)
            iterator += 1
            #print("%.2f %.2f %.2f" % (i,j,k))

        print(arr)
        max = arr.max(axis=0)
        min = arr.min(axis=0)
        print("max = ", max)
        print("min = ", min)
        print("dimensions = ", max-min)
        print("count = ", vertices_count/3)

    @ Slot(QImage)
    def model(self, reply):
        reply.mirrored()
        image = QPixmap.fromImage(reply)

        #global ref_to_img_widget
        #img = ref_to_img_widget.addPixmap(image)
        #img.setPos(0, -500)
        # ref_to_img_widget.update()


pyobject = Test()


class Model3dWidget(QQuickWidget):
    def __init__(self):
        super().__init__()
        global provider
        global windowProvider
        self.engine().rootContext().setContextProperty(
            "_renderCaptureProvider", pyobject)
        self.engine().rootContext().setContextProperty("r_manager", provider)
        self.engine().rootContext().setContextProperty("window_manager", windowProvider)
        self.setSource(QUrl.fromLocalFile("main.qml"))
        self.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
