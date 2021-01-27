import numpy as np
from PySide2.QtGui import QPixmap, QImage, QVector3D
from PySide2.QtCore import Signal, Property, Slot, QUrl, QObject
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtWidgets import QSizePolicy
from PySide2.Qt3DRender import (Qt3DRender)
from Settings import Settings
from Controller import Controller


class ToModelManipulation(QObject):
    xLocationChangeSig = Signal(float)
    yLocationChangeSig = Signal(float)
    zLocationChangeSig = Signal(float)
    originChangeSig = Signal(list)
    xRotationChangeSig = Signal(float)
    yRotationChangeSig = Signal(float)
    zRotationChangeSig = Signal(float)
    xScaleChangeSig = Signal(float)
    yScaleChangeSig = Signal(float)
    zScaleChangeSig = Signal(float)

    def __init__(self, parent=None):
        super(ToModelManipulation, self).__init__(parent)
        contr = Controller()
        contr.addSend("3d/model/location/x", self.xLocationChangeSig)
        contr.addSend("3d/model/location/y", self.yLocationChangeSig)
        contr.addSend("3d/model/location/z", self.zLocationChangeSig)
        contr.addSend("3d/model/origin", self.originChangeSig)
        contr.addSend("3d/model/rotation/x", self.xRotationChangeSig)
        contr.addSend("3d/model/rotation/y", self.yRotationChangeSig)
        contr.addSend("3d/model/rotation/z", self.zRotationChangeSig)
        contr.addSend("3d/model/scale/x", self.xScaleChangeSig)
        contr.addSend("3d/model/scale/y", self.yScaleChangeSig)
        contr.addSend("3d/model/scale/z", self.zScaleChangeSig)

    def sendLocations(self, x: float, y: float, z: float):
        self.xLocationChangeSig.emit(x)
        self.yLocationChangeSig.emit(y)
        self.zLocationChangeSig.emit(z)

        self.xRotationChangeSig.emit(0)
        self.yRotationChangeSig.emit(0)
        self.zRotationChangeSig.emit(0)
        self.xScaleChangeSig.emit(100)
        self.yScaleChangeSig.emit(100)
        self.zScaleChangeSig.emit(100)

    def sendOrigin(self, x: float, y: float, z: float):
        origin = [round(x, 2),
                  round(y, 2),
                  round(z, 2)]
        self.originChangeSig.emit(origin)


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
    originChanged = Signal(QVector3D)

    def __init__(self, parent=None):
        super(MeshManager, self).__init__(parent)
        contr = Controller()
        contr.addRecive("3d/model/path", self.set_modelChange)
        contr.addRecive("3d/model/bounding", self.set_model_on_center)
        contr.addRecive("3d/model/location/x", self.set_x)
        contr.addRecive("3d/model/location/y", self.set_y)
        contr.addRecive("3d/model/location/z", self.set_z)
        contr.addRecive("3d/model/rotation/x", self.set_x_rot)
        contr.addRecive("3d/model/rotation/y", self.set_y_rot)
        contr.addRecive("3d/model/rotation/z", self.set_z_rot)
        contr.addRecive("3d/model/scale/x", self.set_x_scale)
        contr.addRecive("3d/model/scale/y", self.set_y_scale)
        contr.addRecive("3d/model/scale/z", self.set_z_scale)

        self.send = ToModelManipulation()

        self.bedX = 0
        self.bedY = 0
        self._x = 0
        self._y = 0
        self._z = 0
        self._x_rot = 0
        self._y_rot = 0
        self._z_rot = 0
        self._x_scale = 1
        self._y_scale = 1
        self._z_scale = 1
        self._modelChange = ""
        self._origin = [0, 0, 0]
        self.loadSettings()

    def loadSettings(self):
        settings = Settings()
        self.bedX = float(settings.printerSettings['bed_size_x'])
        self.bedY = float(settings.printerSettings['bed_size_x'])

    @Property(float, notify=xChanged)
    def x(self):
        return self._x

    @Slot(float)
    def set_x(self, new_x):
        print("nowe x", new_x)
        new_x = round(new_x, 1)
        if self._x != new_x:
            self._x = new_x
            self.xChanged.emit(new_x)
            self.send.xLocationChangeSig.emit(new_x)

    @Property(float, notify=yChanged)
    def y(self):
        return self._y

    @Slot(float)
    def set_y(self, new_y):
        new_y = round(new_y, 1)
        if self._y != new_y:
            self._y = new_y
            self.yChanged.emit(new_y)
            self.send.yLocationChangeSig.emit(new_y)

    @Property(float, notify=zChanged)
    def z(self):
        return self._z

    @Slot(float)
    def set_z(self, new_z):
        if self._z != new_z:
            self._z = new_z
            self.zChanged.emit(new_z)

    # rotation
    @Property(float, notify=x_rot_Changed)
    def x_rot(self):
        return self._x_rot

    def set_x_rot(self, angle):
        if self._x_rot != angle:
            self._x_rot = angle
            self.x_rot_Changed.emit(angle)

    @Property(float, notify=y_rot_Changed)
    def y_rot(self):
        return self._y_rot

    def set_y_rot(self, angle):
        if self._y_rot != angle:
            self._y_rot = angle
            self.y_rot_Changed.emit(angle)

    @Property(float, notify=z_rot_Changed)
    def z_rot(self):
        return self._z_rot

    def set_z_rot(self, angle):
        if self._z_rot != angle:
            self._z_rot = angle
            self.z_rot_Changed.emit(angle)

    # scale
    @Property(float, notify=x_scale_Changed)
    def x_scale(self):
        return self._x_scale

    def set_x_scale(self, angle):
        angle = angle/100.0
        if self._x_scale != angle:
            self._x_scale = angle
            self.x_scale_Changed.emit(angle)

    @Property(float, notify=y_scale_Changed)
    def y_scale(self):
        return self._y_scale

    def set_y_scale(self, angle):
        angle = angle/100.0
        if self._y_scale != angle:
            self._y_scale = angle
            self.y_scale_Changed.emit(angle)

    @Property(float, notify=z_scale_Changed)
    def z_scale(self):
        return self._z_scale

    def set_z_scale(self, angle):
        angle = angle/100.0
        if self._z_scale != angle:
            self._z_scale = angle
            self.z_scale_Changed.emit(angle)

    # origin
    @Property(QVector3D, notify=originChanged)
    def origin(self):
        return QVector3D(self._origin[0], self._origin[1], self._origin[2])

    def set_origin(self, x, y, z):
        self._origin = [round(x, 2),
                        round(y, 2),
                        round(z, 2)]
        self.originChanged.emit(
            QVector3D(self._origin[0], self._origin[1], self._origin[2]))

    # model

    @Property(str, notify=modelChanged)
    def modelChange(self):
        return self._modelChange

    def set_modelChange(self, path):
        if self._modelChange != path:
            self._modelChange = path
            self.modelChanged.emit(path)

    def set_model_on_center(self, min, max):
        x = (min[0] + max[0]) / 2
        y = (min[1] + max[1]) / 2
        new_x = (self.bedX/2)-x
        new_y = (self.bedY/2)-y
        new_z = -min[2]
        self.set_x(new_x)  # propraw
        self.set_y(new_y)
        self.set_z(new_z)
        self.send.sendOrigin(min[0], min[1], min[2])
        self.set_origin(min[0], min[1], min[2])
        self.send.sendLocations(new_x, new_y, new_z)


class BedManager(QObject):
    xBedChanged = Signal(float)
    yBedChanged = Signal(float)

    def __init__(self, parent=None):
        super(BedManager, self).__init__(parent)
        self._xBed = 235
        self._yBed = 235
        self.loadSettings()
        contr = Controller()
        contr.addRecive("3d/bedSize", self.set_bed)

    def loadSettings(self):
        settings = Settings()
        self._xBed = float(settings.printerSettings['bed_size_x'])
        self._yBed = float(settings.printerSettings['bed_size_x'])

    @Property(float, notify=xBedChanged)
    def xBed(self):
        return self._xBed

    @Property(float, notify=yBedChanged)
    def yBed(self):
        return self._yBed

    def set_bed(self, new_x, new_y):
        print("New bed", new_x, new_y)
        self._xBed = new_x
        self.xBedChanged.emit(new_x)
        self._yBed = new_y
        self.yBedChanged.emit(new_y)


class MeshUtils(QObject):
    trisCountChangeSig = Signal(int)
    dimensionChangeSig = Signal(float, float, float)
    boundingChangeSig = Signal(list, list)
    imageChangeSig = Signal(QPixmap)

    def __init__(self):
        super(MeshUtils, self).__init__()
        contr = Controller()
        contr.addSend("3d/model/tris", self.trisCountChangeSig)
        contr.addSend("3d/model/dimension", self.dimensionChangeSig)
        contr.addSend("3d/model/bounding", self.boundingChangeSig)
        contr.addSend("3d/view/top", self.imageChangeSig)

    @ Slot(Qt3DRender.QGeometry)
    def get_geometry(self, reply):
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
            # print("%.2f %.2f %.2f" % (i,j,k))

        # print(arr)
        size_min = arr.min(axis=0)
        size_max = arr.max(axis=0)
        self.boundingChangeSig.emit(size_min, size_max)

        print("count = ", vertices_count/3)
        self.trisCountChangeSig.emit(int(vertices_count/3))

        x, y, z = (abs(size_max)+abs(size_min))
        self.dimensionChangeSig.emit(x, y, z)

    @ Slot(QImage)
    def model(self, reply):
        reply.mirrored()
        image = QPixmap.fromImage(reply)
        self.imageChangeSig.emit(image)
        # global ref_to_img_widget
        # img = ref_to_img_widget.addPixmap(image)
        # img.setPos(0, -500)
        # ref_to_img_widget.update()


pyobject = MeshUtils()


class Model3dWidget(QQuickWidget):
    modelChangePathSig = Signal(str)
    modelChangeNameSig = Signal(str)

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addSend("3d/model/path", self.modelChangePathSig)
        contr.addSend("3d/model/name", self.modelChangeNameSig)

        self.setAcceptDrops(True)
        provider = MeshManager()
        bed = BedManager()
        self.engine().rootContext().setContextProperty(
            "_renderCaptureProvider", pyobject)
        self.engine().rootContext().setContextProperty("r_manager", provider)
        self.engine().rootContext().setContextProperty("window_manager", bed)
        self.setSource(QUrl.fromLocalFile("qml/main.qml"))
        # self.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def dragMoveEvent(self, e):
        e.acceptProposedAction()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ingore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        fname = urls[0].toLocalFile()
        tmp = fname.rsplit('/', 1)
        self.modelChangeNameSig.emit(tmp[-1])
        self.modelChangePathSig.emit("file:///"+fname)
