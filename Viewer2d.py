from PySide2.QtWidgets import QGraphicsView, QGraphicsScene
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
from PIL.ImageQt import ImageQt
from PIL import Image
im = Image.open("images/tex.jpg")
im = im.convert('L')

ref_to_img_widget = None


class ImageWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self._zoom = 0
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scale(1,-1) #tuaj
        self.scene = QGraphicsScene()
        global ref_to_img_widget
        ref_to_img_widget = self.scene
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
