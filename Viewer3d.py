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
    bottomLeftOriginChanged = Signal(QVector3D)

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
        contr.addRecive("3d/model/rotation/z", self.set_z_rot)
        contr.addRecive("3d/model/scale/x", self.set_x_scale)
        contr.addRecive("3d/model/scale/y", self.set_y_scale)
        contr.addRecive("3d/model/scale/z", self.set_z_scale)
        contr.addRecive("3d/bedSize", self.set_bed)
        self.send = ToModelManipulation()
        self.bedX = 0
        self.bedY = 0
        self._modelChange = ""
        self._matrix = QMatrix4x4(
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
        self._origin = [0, 0, 0]
        self._translation = np.zeros(3, dtype=np.float32)
        self._rotation = np.zeros(3, dtype=np.float32)
        self._scale = np.ones(3, dtype=np.float32)
        self._bottomLeftOrigin = [0, 0, 0, 0, 0, 0]
        self.loadSettings()

    def loadSettings(self):
        settings = Settings()
        self.bedX = float(settings.printerSettings['bed_size_x'])
        self.bedY = float(settings.printerSettings['bed_size_x'])

    def set_bed(self, x, y):
        self.bedX = x
        self.bedY = y

    @Property(str, notify=modelChanged)
    def modelChange(self):
        return self._modelChange

    def set_modelChange(self, path):
        if self._modelChange != path:
            self._modelChange = path
            self._translation = np.zeros(3, dtype=np.float32)
            self._rotation = np.zeros(3, dtype=np.float32)
            self._scale = np.ones(3, dtype=np.float32)
            self.modelChanged.emit(path)

    @Property(QMatrix4x4, notify=matrixChanged)
    def matrix(self):
        return self._matrix

    @Slot(QMatrix4x4)
    def set_matrix(self, matrix):
        m = matrix
        m = np.dot(m, np.array([[1, 0, 0, 0], [0, 0, 1, 0], [
                   0, -1, 0, 0], [0, 0, 0, 1]]))  # rotation x -90
        m = m.flatten()
        # print("matrix = ", m)
        self._matrix = QMatrix4x4(m)
        self.matrixChanged.emit(self._matrix)

    @Slot(float)
    def set_x(self, new_x):
        new_x = round(new_x, 2)
        if new_x != self._translation[0]:
            self._translation[0] = new_x
            self.transformation()
            self.send.xLocationChangeSig.emit(new_x)

    @Slot(float)
    def set_y(self, new_y):
        new_y = round(new_y, 2)
        if new_y != self._translation[2]:
            self._translation[2] = -new_y
            self.transformation()
            self.send.yLocationChangeSig.emit(new_y)

    @Slot(float)
    def set_z(self, new_z):
        new_z = round(new_z, 2)
        if new_z != self._translation[1]:
            self._translation[1] = new_z
            self.transformation()
            self.send.zLocationChangeSig.emit(new_z)

    @Slot(float)
    def set_x_rot(self, angle):
        self._rotation[0] = angle
        self.transformation()
        self.send.xRotationChangeSig.emit(angle)

    @Slot(float)
    def set_y_rot(self, angle):
        self._rotation[2] = angle
        self.transformation()
        self.send.yRotationChangeSig.emit(angle)

    @Slot(float)
    def set_z_rot(self, angle):
        self._rotation[1] = angle
        self.transformation()
        self.send.zRotationChangeSig.emit(angle)

    @Slot(float)
    def set_x_scale(self, percente):
        percente = percente/100
        self._scale[0] = percente
        self.transformation()
        self.send.xScaleChangeSig.emit(percente)

    @Slot(float)
    def set_y_scale(self, percente):
        percente = percente/100
        self._scale[1] = percente
        self.transformation()
        self.send.yScaleChangeSig.emit(percente)

    @Slot(float)
    def set_z_scale(self, percente):
        percente = percente/100
        self._scale[2] = percente
        self.transformation()
        self.send.zScaleChangeSig.emit(percente)

    def transformation(self):
        sinX = np.sin(np.deg2rad(self._rotation[0]))
        cosX = np.cos(np.deg2rad(self._rotation[0]))

        sinY = np.sin(np.deg2rad(self._rotation[1]))
        cosY = np.cos(np.deg2rad(self._rotation[1]))

        sinZ = np.sin(np.deg2rad(self._rotation[2]))
        cosZ = np.cos(np.deg2rad(self._rotation[2]))

        transfor_arr = np.array([[1, 0, 0, self._origin[0]],
                                 [0, 1, 0, self._origin[2]],
                                 [0, 0, 1, -self._origin[1]],
                                 [0, 0, 0, 1]])

        rotation_z_arr = np.array([[cosZ, -sinZ, 0, 0],
                                   [sinZ,  cosZ, 0, 0],
                                   [0,        0, 1, 0],
                                   [0,        0, 0, 1]])

        rotation_y_arr = np.array([[cosY,  0, sinY,  0],
                                   [0,     1,    0,  0],
                                   [-sinY, 0, cosY,  0],
                                   [0,     0,    0,  1]])

        rotation_x_arr = np.array([[1,    0,     0, 0],
                                   [0, cosX, -sinX, 0],
                                   [0, sinX,  cosX, 0],
                                   [0,    0,     0, 1]])

        transfor_back_arr = np.array([[1, 0, 0, -self._origin[0]],
                                      [0, 1, 0, -self._origin[2]],
                                      [0, 0, 1, self._origin[1]],
                                      [0, 0, 0, 1]])

        scale_arr = np.array([[self._scale[0], 0, 0, 0],
                              [0, self._scale[2], 0, 0],
                              [0, 0, self._scale[1], 0],
                              [0, 0,             0, 1]])

        move_matrix = np.array([[1, 0, 0, self._translation[0]],
                                [0, 1, 0, self._translation[1]],
                                [0, 0, 1, self._translation[2]],
                                [0, 0, 0, 1]])

        tmp = np.identity(4, dtype=np.float32)
        tmp = np.dot(transfor_arr, tmp)
        tmp = np.dot(scale_arr, tmp)
        tmp = np.dot(rotation_z_arr, tmp)
        tmp = np.dot(rotation_y_arr, tmp)
        tmp = np.dot(rotation_x_arr, tmp)
        tmp = np.dot(transfor_back_arr, tmp)

        #tmp = np.dot(move_matrix, tmp)
        for i, val in enumerate(self._translation):
            tmp[i][3] = val

        # print(tmp)
        self.set_matrix(tmp)

    @Property(QVector3D, notify=originChanged)
    def origin(self):
        return QVector3D(self._origin[0], self._origin[1], self._origin[2])

    @Property(QVector3D, notify=bottomLeftOriginChanged)
    def bottomLeftOrigin(self):
        return QVector3D(self._bottomLeftOrigin[0], self._bottomLeftOrigin[1], self._bottomLeftOrigin[2])

    def set_central_origin(self, x, y, z):
        self._origin = [round(x, 2),
                        round(y, 2),
                        round(z, 2)]
        self.originChanged.emit(
            QVector3D(self._origin[0], self._origin[1], self._origin[2]))

    def set_bottomLeft_origin(self, x, y, z):
        self._bottomLeftOrigin = [round(x, 2),
                                  round(y, 2),
                                  round(z, 2)]
        self.bottomLeftOriginChanged.emit(
            QVector3D(self._bottomLeftOrigin[0], self._bottomLeftOrigin[1], self._bottomLeftOrigin[2]))

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
        self.set_bottomLeft_origin(min[0], min[1], min[2])
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
        self._yBed = float(settings.printerSettings['bed_size_y'])

    @Property(float, notify=xBedChanged)
    def xBed(self):
        return self._xBed

    @Property(float, notify=yBedChanged)
    def yBed(self):
        return self._yBed

    def set_bed(self, new_x, new_y):
        #print("New bed", new_x, new_y)
        self._xBed = new_x
        self.xBedChanged.emit(new_x)
        self._yBed = new_y
        self.yBedChanged.emit(new_y)


class MeshUtils(QObject):
    trisCountChangeSig = Signal(int)
    dimensionChangeSig = Signal(float, float, float)
    boundingChangeSig = Signal(list, list)
    renderChangeSig = Signal(QPixmap)

    def __init__(self):
        super(MeshUtils, self).__init__()
        contr = Controller()
        contr.addSend("3d/model/tris", self.trisCountChangeSig)
        contr.addSend("3d/model/dimension", self.dimensionChangeSig)
        contr.addSend("3d/model/bounding", self.boundingChangeSig)
        contr.addSend("3d/view/top", self.renderChangeSig)

    @Slot(Qt3DRender.QGeometry)
    def get_geometry(self, reply):
        vertexPosition = None
        atributes = reply.attributes()
        for i in atributes:
            if i.name() == 'vertexPosition':
                vertexPosition = i
        #print("type =", vertexPosition.VertexBaseType())
        #print("offset =", vertexPosition.byteOffset())
        #print("stride =", vertexPosition.byteStride())
        #print("divisior =", vertexPosition.divisor())
        #print("size =", vertexPosition.vertexSize())

        vertices_count = vertexPosition.count()
        tmp = np.frombuffer(vertexPosition.buffer().data(), dtype=np.float32)
        arr = np.empty((0, 3), dtype=np.float32)
        iterator = 1
        for i, j, k in zip(tmp[0::3], tmp[1::3], tmp[2::3]):
            if(iterator % 2):
                arr = np.append(arr, np.array(
                    [[i, j, k]], dtype=np.float32), axis=0)
            iterator += 1
            #print("%.2f %.2f %.2f" % (i, j, k))

        # print(arr)
        size_min = arr.min(axis=0)
        size_max = arr.max(axis=0)
        self.boundingChangeSig.emit(size_min, size_max)

        #print("count = ", vertices_count/3)
        self.trisCountChangeSig.emit(int(vertices_count/3))

        x, y, z = (abs(size_max)+abs(size_min))
        self.dimensionChangeSig.emit(x, y, z)

    @Slot(QImage)
    def render(self, reply):
        reply.mirrored()
        image = QPixmap.fromImage(reply)
        self.renderChangeSig.emit(image)


pyobject = MeshUtils()


class CameraManager(QObject):
    positionVectorChangeSig = Signal(QVector3D)
    viewVectorChangeSig = Signal(QVector3D)
    upVectorChangeSig = Signal(QVector3D)
    _xBed = 0.0
    _yBed = 0.0

    def __init__(self, parent=None):
        super(CameraManager, self).__init__(parent)
        self.loadSettings()
        contr = Controller()
        contr.addRecive("3d/camera/position/home", self.set_camera_home)
        contr.addRecive("3d/camera/position/top", self.set_camera_top)
        contr.addRecive("3d/camera/position/bottom", self.set_camera_bottom)
        contr.addRecive("3d/camera/position/front", self.set_camera_front)
        contr.addRecive("3d/camera/position/back", self.set_camera_back)
        contr.addRecive("3d/camera/position/left", self.set_camera_left)
        contr.addRecive("3d/camera/position/right", self.set_camera_right)
        contr.addRecive("3d/bedSize", self.set_bed)
        bed_longer_edge = self._xBed if self._xBed > self._yBed else self._yBed
        bed_longer_edge *= 1.5
        self._position = QVector3D(self._xBed/2,
                                   bed_longer_edge,
                                   bed_longer_edge)
        self._view = QVector3D(self._xBed/2, 0.0, -self._yBed/2)
        self._rotation = QVector3D(0.0, 1.0, 0.0)  # tilt of camera

    @Property(QVector3D, notify=positionVectorChangeSig)
    def position(self):
        return self._position

    @Property(QVector3D, notify=viewVectorChangeSig)
    def view(self):
        return self._view

    @Property(QVector3D, notify=upVectorChangeSig)
    def rotation(self):
        return self._rotation

    def set_bed(self, new_x, new_y):
        self._xBed = new_x
        self._yBed = new_y
        self.set_camera_home()

    def set_camera(self, position: QVector3D, view: QVector3D, rotation: QVector3D):
        self._position = position
        self._view = view
        self._rotation = rotation
        self.positionVectorChangeSig.emit(position)
        self.viewVectorChangeSig.emit(view)
        self.upVectorChangeSig.emit(rotation)

    def set_camera_home(self):
        bed_longer_edge = self._xBed if self._xBed > self._yBed else self._yBed
        bed_longer_edge *= 1.5
        p = QVector3D(self._xBed/2,
                      bed_longer_edge,
                      bed_longer_edge)
        v = QVector3D(self._xBed/2, 0.0, -self._yBed/2)
        r = QVector3D(0.0, 1.0, 0.0)
        self.set_camera(p, v, r)

    def set_camera_top(self):
        p = QVector3D(self._xBed/2, 500.0, -self._yBed/2)
        v = QVector3D(self._xBed/2, 0.0, -self._yBed/2)
        r = QVector3D(0.0, 0.0, -1.0)
        self.set_camera(p, v, r)

    def set_camera_bottom(self):
        p = QVector3D(self._xBed/2, -500.0, -self._yBed/2)
        v = QVector3D(self._xBed/2, 0.0, -self._yBed/2)
        r = QVector3D(0.0, 0.0, 1.0)
        self.set_camera(p, v, r)

    def set_camera_front(self):
        p = QVector3D(self._xBed/2, 0.0, 500)
        v = QVector3D(self._xBed/2, 0.0, -self._yBed/2)
        r = QVector3D(0.0, 1.0, 0.0)
        self.set_camera(p, v, r)

    def set_camera_back(self):
        p = QVector3D(self._xBed/2, 0.0, -500-self._yBed)
        v = QVector3D(self._xBed/2, 0.0, -self._yBed/2)
        r = QVector3D(0.0, 1.0, 0.0)
        self.set_camera(p, v, r)

    def set_camera_left(self):
        p = QVector3D(-500, 0.0, -self._yBed/2)
        v = QVector3D(self._xBed/2, 0.0, -self._yBed/2)
        r = QVector3D(0.0, 1.0, 0.0)
        self.set_camera(p, v, r)

    def set_camera_right(self):
        p = QVector3D(500+self._xBed, 0.0, -self._yBed/2)
        v = QVector3D(self._xBed/2, 0.0, -self._yBed/2)
        r = QVector3D(0.0, 1.0, 0.0)
        self.set_camera(p, v, r)

    def loadSettings(self):
        settings = Settings()
        self._xBed = float(settings.printerSettings['bed_size_x'])
        self._yBed = float(settings.printerSettings['bed_size_y'])


class Model3dWidget(QQuickWidget):
    modelChangePathSig = Signal(str)
    modelChangeNameSig = Signal(str)
    imageChangePathSig = Signal(str)
    imageChangeNameSig = Signal(str)

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addSend("3d/model/path", self.modelChangePathSig)
        contr.addSend("3d/model/name", self.modelChangeNameSig)
        contr.addSend("2d/image/path", self.imageChangePathSig)
        contr.addSend("2d/image/name", self.imageChangeNameSig)

        self.setAcceptDrops(True)
        provider = TransformationMatrixManager()
        bed = BedManager()
        self.engine().rootContext().setContextProperty(
            "_renderCaptureProvider", pyobject)
        self.engine().rootContext().setContextProperty("r_manager", provider)
        self.engine().rootContext().setContextProperty("window_manager", bed)
        self.engine().rootContext().setContextProperty("cameraManager", CameraManager())
        self.setSource(QUrl.fromLocalFile("qml/main.qml"))
        self.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #print("QQuickWidget size ->", self.size())

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
        name = tmp[-1]
        tmp = name.rsplit('.', 1)
        extension = tmp[-1].lower()
        supportedModelExtensions = ['obj', 'stl', 'ply']
        if any(extension in s for s in supportedModelExtensions):
            self.modelChangeNameSig.emit(name)
            self.modelChangePathSig.emit("file:///"+fname)
        else:
            self.imageChangeNameSig.emit(name)
            self.imageChangePathSig.emit(fname)


if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    iw = Model3dWidget()
    Controller().match()
    iw.show()
    sys.exit(app.exec_())
