from PySide2.QtWidgets import QGraphicsView, QGraphicsItem, QPushButton, QVBoxLayout, QFrame, QHBoxLayout, QGraphicsScene, QApplication, QLabel, QWidget, QAction, QGridLayout
from PySide2.QtGui import QPixmap, QPainter, QIcon, QKeySequence, QBrush, QColor, QTransform
from PySide2.QtCore import Qt, Signal, QSize, QRect, Slot
from PIL.ImageQt import ImageQt
from PIL import Image
from Controller import Controller


class RulerWidget(QWidget):
    def __init__(self, *args):
        super(RulerWidget, self).__init__(*args)
        self.orientation = Qt.Horizontal
        self.firstEdge = False
        self.inv = False
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: lightGrey')

    def setOrientation(self, orientation):
        self.orientation = orientation
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        tick = 0
        while True:
            if tick % 20 == 0:
                if not self._drawTick(painter, tick, 20):
                    break
                self._drawTickLabel(painter, tick, 15)
            elif tick % 10 == 0:
                if not self._drawTick(painter, tick, 5):
                    break
            else:
                if not self._drawTick(painter, tick, 3):
                    break

            tick += 5

    def _drawTick(self, painter, tick, length):
        tick = (550*tick)//200
        if self.firstEdge:
            tickStart = 0
            tickEnd = length

        if self.orientation == Qt.Horizontal:
            if self.inv:
                tick = self.size().width() - tick - 1

            if not (0 <= tick < self.size().width()):
                return False

            if not self.firstEdge:
                tickStart = self.size().height()
                tickEnd = tickStart - length

            painter.drawLine(tick+1, tickStart, tick+1, tickEnd)
        else:
            if self.inv:
                tick = self.size().height() - tick - 1

            if not (0 <= tick < self.size().height()):
                return False

            if not self.firstEdge:
                tickStart = self.size().width()
                tickEnd = tickStart - length

            painter.drawLine(tickStart, tick, tickEnd, tick)

        return True

    def _drawTickLabel(self, painter, tick, pos):
        label = str(tick)
        tick = (550*tick)//200

        if self.orientation == Qt.Horizontal:
            if self.inv:
                tick = self.size().width() - tick - 1

            if self.firstEdge:
                tickStart = pos + 10
            else:
                tickStart = self.size().height() - pos

            textFlags = Qt.TextDontClip | Qt.AlignBottom | Qt.AlignLeft
            rect = QRect(tick + 3, tickStart, 20, 10)
            painter.drawText(rect, textFlags, label)
        else:
            if self.inv:
                tick = self.size().height() - tick - 1

            if self.firstEdge:
                tickStart = pos + 20
            else:
                tickStart = self.size().width() - pos - 20

            textFlags = Qt.TextDontClip | Qt.AlignRight | Qt.AlignLeft
            i = 0
            for letter in label:
                rect = QRect(tickStart+5, tick + i, 20, 10)
                painter.drawText(rect, textFlags, letter)
                i += 10

    def sizeHint(self):
        if self.orientation == Qt.Horizontal:
            return QSize(300, 20)
        else:
            return QSize(20, 300)


class RulerWindow(RulerWidget):
    def __init__(self, *args):
        super(RulerWindow, self).__init__(*args)
        self.setToolTip(
            'Double-click (or press V) to toggle horizontal/vertical.\n'
            'Press arrows to move window by 1 pixel.\n'
            'Press B to toggle borderless.\n'
            'Press R to toggle reverse direction of the ruler.'
        )
        #self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.vertAction = QAction('&Vertical', self)
        self.vertAction.setShortcut(QKeySequence('v'))
        self.vertAction.setCheckable(True)
        self.vertAction.triggered.connect(self.toggleVertical)
        self.addAction(self.vertAction)

        self.borderAction = QAction('&Borderless', self)
        self.borderAction.setShortcut(QKeySequence('b'))
        self.borderAction.setCheckable(True)
        self.borderAction.triggered.connect(self.toggleBorderless)
        self.addAction(self.borderAction)

        self.edgeAction = QAction('First edge', self)
        self.edgeAction.setCheckable(True)
        self.edgeAction.triggered.connect(self.toggleEdge)
        self.addAction(self.edgeAction)

        self.invAction = QAction('&Reverse direction', self)
        self.invAction.setShortcut(QKeySequence('r'))
        self.invAction.setCheckable(True)
        self.invAction.triggered.connect(self.toggleInv)
        self.addAction(self.invAction)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def keyPressEvent(self, event):
        xy = None
        if event.key() == Qt.Key_Left:
            xy = -1, 0
        elif event.key() == Qt.Key_Right:
            xy = 1, 0
        elif event.key() == Qt.Key_Up:
            xy = 0, -1
        elif event.key() == Qt.Key_Down:
            xy = 0, 1

        if xy is None:
            super(RulerWindow, self).keyPressEvent(event)
        else:
            if event.modifiers() & Qt.ShiftModifier:
                self.resize(self.width() + xy[0], self.height() + xy[1])
            else:
                self.move(self.x() + xy[0], self.y() + xy[1])

    def mouseDoubleClickEvent(self, event):
        self.toggleVertical()

    @Slot()
    def toggleVertical(self):
        if self.orientation == Qt.Horizontal:
            self.setOrientation(Qt.Vertical)
            self.vertAction.setChecked(True)
        else:
            self.setOrientation(Qt.Horizontal)
            self.vertAction.setChecked(False)
        self.resize(self.height(), self.width())  # transpose size

    @Slot()
    def toggleBorderless(self):
        size = self.size()

        self.hide()  # seems the flag can't be set when window is visible
        self.setWindowFlags(self.windowFlags() ^ Qt.FramelessWindowHint)
        self.borderAction.setChecked(
            self.windowFlags() & Qt.FramelessWindowHint)
        self.show()

        self.resize(size)

    @Slot()
    def toggleEdge(self):
        self.firstEdge = not self.firstEdge
        self.update()

    @Slot()
    def toggleInv(self):
        self.inv = not self.inv
        self.update()


class ImageWidget(QWidget):
    opacityChangeSig = Signal(int)
    activeToolSig = Signal(str)

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addSend("2d/image/opacity", self.opacityChangeSig)
        contr.addSend("2d/tool", self.activeToolSig)

        buttonSize = QSize(40, 40)
        iconSize = QSize(32, 32)

        freeButton = QPushButton()
        freeButton.setIcon(QIcon("icons/2d_free.png"))
        freeButton.setFixedSize(buttonSize)
        freeButton.setIconSize(iconSize)
        freeButton.setCheckable(True)
        freeButton.setChecked(True)
        freeButton.clicked.connect(self.freeButtonActive)

        moveButton = QPushButton()
        moveButton.setIcon(QIcon("icons/2d_move.png"))
        moveButton.setFixedSize(buttonSize)
        moveButton.setIconSize(iconSize)
        moveButton.setCheckable(True)
        moveButton.clicked.connect(self.moveButtonActive)

        rotationButton = QPushButton()
        rotationButton.setIcon(QIcon("icons/2d_rotate.png"))
        rotationButton.setFixedSize(buttonSize)
        rotationButton.setIconSize(iconSize)
        rotationButton.setCheckable(True)
        rotationButton.clicked.connect(self.rotationButtonActive)

        scaleButton = QPushButton()
        scaleButton.setIcon(QIcon("icons/2d_scale.png"))
        scaleButton.setFixedSize(buttonSize)
        scaleButton.setIconSize(iconSize)
        scaleButton.setCheckable(True)
        scaleButton.clicked.connect(self.scaleButtonActive)

        hideButton = QPushButton()
        hideButton.setIcon(QIcon("icons/2d_hide.png"))
        hideButton.setFixedSize(buttonSize)
        hideButton.setIconSize(iconSize)
        hideButton.setCheckable(True)
        hideButton.clicked.connect(self.hideButtonActive)
        hideButton.setShortcut(QKeySequence('h'))
        hideButton.setToolTip('Hide (H)')

        self.toolButtons = [freeButton, moveButton,
                            rotationButton, scaleButton]

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(freeButton)
        buttonLayout.addWidget(moveButton)
        buttonLayout.addWidget(rotationButton)
        buttonLayout.addWidget(scaleButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(hideButton)
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(Container())
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

    def freeButtonActive(self):
        for i in self.toolButtons:
            i.setChecked(False)
        self.sender().setChecked(True)
        self.activeToolSig.emit("free")

    def moveButtonActive(self):
        for i in self.toolButtons:
            i.setChecked(False)
        self.sender().setChecked(True)
        self.activeToolSig.emit("move")

    def rotationButtonActive(self):
        for i in self.toolButtons:
            i.setChecked(False)
        self.sender().setChecked(True)
        self.activeToolSig.emit("rotation")

    def scaleButtonActive(self):
        for i in self.toolButtons:
            i.setChecked(False)
        self.sender().setChecked(True)
        self.activeToolSig.emit("scale")

    def hideButtonActive(self):
        if self.sender().isChecked():
            self.opacityChangeSig.emit(0)
            self.sender().setChecked(True)
        else:
            self.opacityChangeSig.emit(100)
            self.sender().setChecked(False)


class Container(QWidget):
    def __init__(self):
        super().__init__()
        top = RulerWidget()
        left = RulerWidget()
        left.setOrientation(Qt.Vertical)
        left.inv = True
        img = Image2dView()
        fake = QWidget()
        fake.setAttribute(Qt.WA_StyledBackground, True)
        fake.setStyleSheet('background-color: lightGrey')
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(fake, 0, 0)
        layout.addWidget(top, 0, 1)
        layout.addWidget(left, 1, 0)
        layout.addWidget(img, 1, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


class Image2dView(QGraphicsView):
    modelChangePathSig = Signal(str)
    modelChangeNameSig = Signal(str)
    imageChangePathSig = Signal(str)
    imageChangeNameSig = Signal(str)
    imageChangeSig = Signal(QPixmap)

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addRecive('2d/image/opacity', self.setOpacity)
        contr.addRecive('2d/image/path', self.openImage)
        contr.addRecive("2d/tool", self.setTool)
        contr.addRecive("2d/image/off", self.updateImage)
        contr.addRecive("2d/image/location/x", self.set_x)
        contr.addRecive("2d/image/scale/x", self.set_scale)
        contr.addSend("2d/image", self.imageChangeSig)
        contr.addSend("3d/model/path", self.modelChangePathSig)
        contr.addSend("3d/model/name", self.modelChangeNameSig)
        #contr.addSend("2d/image/path", self.imageChangePathSig)
        contr.addSend("2d/image/name", self.imageChangeNameSig)
        contr.addRecive('3d/view/top', self.addCameraImage)

        self.setAcceptDrops(True)
        self._zoom = 0
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)

        self.tool = None

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 550, 550)
        print(self.size())
        self.setAlignment(Qt.AlignBottom | Qt.AlignLeft)

        self.render = self.scene.addPixmap(QPixmap())
        self.texture = self.scene.addPixmap(QPixmap())
        self.setScene(self.scene)
        self.x = 0
        self.y = 0

    def drawBackground(self, painter, rect):
        background_brush = QBrush(QColor(153, 153, 153), Qt.SolidPattern)
        painter.fillRect(rect, background_brush)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)

    def addCameraImage(self, image):
        if image.size().width() == 0:
            return
        #print("render size ->", image.size())
        image = image.scaled(
            550, 550, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        image.save('test.png')
        self.render.setPixmap(image)
        self.scene.update()

    def set_x(self, x):
        self.x = (550*x)//200
        self.updateCoord()

    def set_scale(self, scale):
        scale = scale/100
        self.texture.setScale(scale)
        print(self.texture.shape())
        #self.y = 550-self.texture.height()
        # self.scene.update()
        print("new location", scale)

    def updateImage(self, image):
        self.texture.setPixmap(image)
        self.scene.update()

    def updateCoord(self):
        self.texture.setPos(self.x, self.y)

    def openImage(self, image):
        im = Image.open(image)
        im = im.convert('L')
        qim = ImageQt(im)
        pixmap = QPixmap.fromImage(qim)
        self.texture.setPixmap(pixmap)
        self.texture.setPos(0, 550-pixmap.height())
        self.x = 0
        self.y = 550-pixmap.height()
        self.texture.setZValue(1)
        self.texture.setOpacity(.5)
        if self.tool == 'move':
            self.texture.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.texture.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.imageChangeSig.emit(pixmap)

    def setOpacity(self, value):
        self.texture.setOpacity(value)

    def setTool(self, tool):
        if tool == 'move':
            self.texture.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.texture.setFlag(QGraphicsItem.ItemIsSelectable, True)
        else:
            self.texture.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.texture.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.tool = tool

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
            self.openImage(fname)
            # self.imageChangePathSig.emit("file:///"+fname)


if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    iw = ImageWidget()
    Controller().match()
    Controller().showConnections()
    iw.show()
    sys.exit(app.exec_())
