from PySide2.QtWidgets import QGraphicsView, QGraphicsScene
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Signal
from PIL.ImageQt import ImageQt
from PIL import Image
from Controller import Controller
im = Image.open("images/tex.jpg")
im = im.convert('L')


class ImageWidget(QGraphicsView):
    modelChangePathSig = Signal(str)
    modelChangeNameSig = Signal(str)

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addRecive('2d/opacity', self.setOpacity)
        contr.addSend("3d/model/path", self.modelChangePathSig)
        contr.addSend("3d/model/name", self.modelChangeNameSig)
        contr.addRecive('3d/view/top', self.addCameraItem)

        self.setAcceptDrops(True)
        self._zoom = 0
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scale(1,-1) #tuaj
        self.scene = QGraphicsScene()
        global im
        qim = ImageQt(im)
        self.pixmap = QPixmap.fromImage(qim)
        #img = QImage("images/tex.jpg")
        # img.fill(QColor("red").rgba())
        #pixmap02 = QPixmap.fromImage(img)
        self.item1 = self.scene.addPixmap(self.pixmap)
        self.item1.setPos(0, -256)
        self.item1.setZValue(1)
        self.item1.setOpacity(.5)
        self.scene.setSceneRect(0, -500, 500, 500)
        self.setScene(self.scene)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)

    def addCameraItem(self, image):
        img = self.scene.addPixmap(image)
        img.setPos(0, -500)
        self.scene.update()

    def setOpacity(self, value):
        self.item1.setOpacity(value)

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
