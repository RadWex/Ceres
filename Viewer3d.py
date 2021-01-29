import numpy as np
from PySide2.QtGui import QPixmap, QImage, QVector3D, QMatrix4x4
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
        contr.addSend("3d/model/location/x/set", self.xLocationChangeSig)
        contr.addSend("3d/model/location/y/set", self.yLocationChangeSig)
        contr.addSend("3d/model/location/z/set", self.zLocationChangeSig)
        contr.addSend("3d/model/origin", self.originChangeSig)
        contr.addSend("3d/model/rotation/x/set", self.xRotationChangeSig)
        contr.addSend("3d/model/rotation/y/set", self.yRotationChangeSig)
        contr.addSend("3d/model/rotation/z/set", self.zRotationChangeSig)
        contr.addSend("3d/model/scale/x/set", self.xScaleChangeSig)
        contr.addSend("3d/model/scale/y/set", self.yScaleChangeSig)
        contr.addSend("3d/model/scale/z/set", self.zScaleChangeSig)

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


class TransformationMatrixManager(QObject):
    modelChanged = Signal(str)
    matrixChanged = Signal(QMatrix4x4)
    originChanged = Signal(QVector3D)

    def __init__(self, parent=None):
        super(TransformationMatrixManager, self).__init__(parent)
        contr = Controller()
        contr.addRecive("3d/model/path", self.set_modelChange)
        contr.addRecive("3d/model/bounding", self.set_model_on_center)
        contr.addRecive("3d/model/location/x", self.set_x)
        contr.addRecive("3d/model/location/y", self.set_y)
        contr.addRecive("3d/model/location/z", self.set_z)
        contr.addRecive("3d/model/rotation/x", self.set_x_rot)
        contr.addRecive("3d/model/rotation/y", self.set_y_rot)
        # contr.addRecive("3d/model/rotation/z", self.set_z_rot)
        # contr.addRecive("3d/model/scale/x", self.set_x_scale)
        # contr.addRecive("3d/model/scale/y", self.set_y_scale)
        # contr.addRecive("3d/model/scale/z", self.set_z_scale)
        self.send = ToModelManipulation()
        self.bedX = 0
        self.bedY = 0
        self._modelChange = ""
        self._matrix = QMatrix4x4(
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
        self._matrixPython = np.identity(4, dtype=np.float32)
        self._origin = [0, 0, 0]
        self.loadSettings()

    def loadSettings(self):
        settings = Settings()
        self.bedX = float(settings.printerSettings['bed_size_x'])
        self.bedY = float(settings.printerSettings['bed_size_x'])

    @Property(str, notify=modelChanged)
    def modelChange(self):
        return self._modelChange

    def set_modelChange(self, path):
        if self._modelChange != path:
            self._modelChange = path
            self.modelChanged.emit(path)

    @Property(QMatrix4x4, notify=matrixChanged)
    def matrix(self):
        return self._matrix

    @Slot(QMatrix4x4)
    def set_matrix(self):
        m = self._matrixPython
        m = np.dot(m, np.array([[1, 0, 0, 0], [0, 0, 1, 0], [
                   0, -1, 0, 0], [0, 0, 0, 1]]))  # rotation x -90
        m = m.flatten()
        # print("matrix = ", m)
        self._matrix = QMatrix4x4(m)
        self.matrixChanged.emit(self._matrix)

    @Slot(float)
    def set_x(self, new_x):
        new_x = round(new_x, 2)
        if new_x != self._matrixPython[0][3]:
            self._matrixPython[0][3] = new_x
            self.set_matrix()
            self.send.xLocationChangeSig.emit(new_x)

    @Slot(float)
    def set_y(self, new_y):
        new_y = round(new_y, 2)
        if new_y != self._matrixPython[2][3]:
            self._matrixPython[2][3] = -new_y
            self.set_matrix()
            self.send.yLocationChangeSig.emit(new_y)

    @Slot(float)
    def set_z(self, new_z):
        new_z = round(new_z, 1)
        if new_z != self._matrixPython[1][3]:
            self._matrixPython[1][3] = new_z
            self.set_matrix()
            self.send.zLocationChangeSig.emit(new_z)

    @Slot(float)
    def set_x_rot(self, angle):
        sin = np.sin(np.deg2rad(angle))
        cos = np.cos(np.deg2rad(angle))
        transfor_arr = np.array([[1, 0, 0, self._origin[0]],
                                 [0, 1, 0, self._origin[2]],
                                 [0, 0, 1, -self._origin[1]],
                                 [0, 0, 0, 1]])

        rotation_arr = np.array([[1,   0,   0,  0],
                                 [0, cos, -sin, 0],
                                 [0, sin,  cos, 0],
                                 [0,   0,   0,  1]])

        transfor_back_arr = np.array([[1, 0, 0, -self._origin[0]],
                                      [0, 1, 0, -self._origin[2]],
                                      [0, 0, 1, self._origin[1]],
                                      [0, 0, 0, 1]])
        self._matrixPython = np.dot(self._matrixPython, transfor_arr)
        self._matrixPython = np.dot(self._matrixPython, rotation_arr)
        self._matrixPython = np.dot(self._matrixPython, transfor_back_arr)
        self.set_matrix()
        self.send.xRotationChangeSig.emit(angle)

    @Slot(float)
    def set_y_rot(self, angle):
        sin = np.sin(np.deg2rad(angle))
        cos = np.cos(np.deg2rad(angle))
        transfor_arr = np.array([[1, 0, 0,  self._origin[0]],
                                 [0, 1, 0,  self._origin[2]],
                                 [0, 0, 1, -self._origin[1]],
                                 [0, 0, 0, 1]])

        rotation_arr = np.array([[cos,  0, sin,  0],
                                 [0,    1,   0,  0],
                                 [-sin, 0, cos,  0],
                                 [0,    0,   0,  1]])

        transfor_back_arr = np.array([[1, 0, 0, -self._origin[0]],
                                      [0, 1, 0, -self._origin[2]],
                                      [0, 0, 1,  self._origin[1]],
                                      [0, 0, 0, 1]])
        self._matrixPython = np.dot(self._matrixPython, transfor_arr)
        self._matrixPython = np.dot(self._matrixPython, rotation_arr)
        self._matrixPython = np.dot(self._matrixPython, transfor_back_arr)
        self.set_matrix()
        self.send.yRotationChangeSig.emit(angle)

    @ Property(QVector3D, notify=originChanged)
    def origin(self):
        return QVector3D(self._origin[0], self._origin[1], self._origin[2])

    def set_central_origin(self, x, y, z):
        self._origin = [round(x, 2),
                        round(y, 2),
                        round(z, 2)]
        self.originChanged.emit(
            QVector3D(self._origin[0], self._origin[1], self._origin[2]))

    def set_model_on_center(self, min, max):
        x = (min[0] + max[0]) / 2
        y = (min[1] + max[1]) / 2
        z = (min[2] + max[2]) / 2
        new_x = (self.bedX/2)-x
        new_y = (self.bedY/2)-y
        new_z = -min[2]
        self.set_x(new_x)  # propraw
        self.set_y(new_y)
        self.set_z(new_z)
        self.send.sendOrigin(min[0], min[1], min[2])
        self.set_central_origin(x, y, z)
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

    @ Property(float, notify=xBedChanged)
    def xBed(self):
        return self._xBed

    @ Property(float, notify=yBedChanged)
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
        provider = TransformationMatrixManager()
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
