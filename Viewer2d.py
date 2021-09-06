from PySide2.QtWidgets import QGraphicsView, QGraphicsItem, QPushButton, QVBoxLayout, QFrame, QHBoxLayout, QGraphicsScene, QApplication, QLabel, QWidget, QAction, QGridLayout, QDockWidget, QMainWindow
from PySide2.QtGui import QPixmap, QPainter, QIcon, QKeySequence, QBrush, QColor, QTransform
from PySide2.QtCore import Qt, Signal, QSize, QRect, Slot, QPointF
from PIL.ImageQt import ImageQt
from PIL import Image
from Controller import Controller
from Settings import Settings


class RulerWidget(QWidget):
    def __init__(self, length):
        super().__init__()
        self.length = length
        self.loadSettings()
        contr = Controller()
        contr.addRecive("3d/bedSize", self.set_bed)
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
        tick = (self.length*tick)//self._xBed
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
        tick = (self.length*tick)//self._xBed

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

    def loadSettings(self):
        settings = Settings()
        self._xBed = float(settings.printerSettings['bed_size_x'])
        self._yBed = float(settings.printerSettings['bed_size_y'])

    def set_bed(self, new_x, new_y):
        self._xBed = new_x
        self._yBed = new_y
        self.update()


class RulerWindow(RulerWidget):
    def __init__(self, *args):
        super(RulerWindow, self).__init__(*args)
        self.setToolTip(
            'Double-click (or press V) to toggle horizontal/vertical.\n'
            'Press arrows to move window by 1 pixel.\n'
            'Press B to toggle borderless.\n'
            'Press R to toggle reverse direction of the ruler.'
        )
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

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


class TEST_docking(QMainWindow):
    # TODO DELETE (not used)
    def __init__(self):
        super().__init__()
        self.items = QDockWidget("Dockable", self)

        self.items.setWidget(ImageToolsWidget())
        self.items.setFloating(False)
        self.setCentralWidget(ImageWidget())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.items)
        mainLayout = QHBoxLayout()
        # mainLayout.addWidget(ImageToolsWidget())
        # mainLayout.addWidget(ImageWidget())
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)


class ImageToolsWidget(QWidget):
    hideChangeSig = Signal()
    activeToolSig = Signal(str)

    def __init__(self):
        super().__init__()
        contr = Controller()
        contr.addSend("2d/image/hide", self.hideChangeSig)
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

        buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(buttonLayout)

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
            self.hideChangeSig.emit()
            self.sender().setChecked(True)
        else:
            self.hideChangeSig.emit()
            self.sender().setChecked(False)


class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        initWorkspaceSizeX = 550
        initWorkspaceSizeY = 550

        top = RulerWidget(initWorkspaceSizeX)
        left = RulerWidget(initWorkspaceSizeY)
        left.setOrientation(Qt.Vertical)
        left.inv = True

        img = Image2dView(initWorkspaceSizeX, initWorkspaceSizeY)
        blind_spot_ruler = QWidget()
        blind_spot_ruler.setAttribute(Qt.WA_StyledBackground, True)
        blind_spot_ruler.setStyleSheet('background-color: lightGrey')
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(blind_spot_ruler, 0, 0)
        layout.addWidget(top, 0, 1)
        layout.addWidget(left, 1, 0)
        layout.addWidget(img, 1, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        # DEBUG
        img.openImage("1.png")
        img.set_x(20)
        img.set_y(40)
        img.set_scale(20)
        ###
        self.setLayout(layout)


class Image2dView(QGraphicsView):
    modelChangePathSig = Signal(str)
    modelChangeNameSig = Signal(str)
    imageChangePathSig = Signal(str)
    imageChangeNameSig = Signal(str)
    imageChangeSig = Signal(QPixmap)
    imageChangeLocX = Signal(float)
    imageChangeLocY = Signal(float)

    def __init__(self, sizeX, sizeY):
        super().__init__()
        contr = Controller()
        contr.addRecive('2d/image/opacity', self.setOpacity)
        contr.addRecive('2d/image/hide', self.hideUnhide)
        contr.addRecive('2d/image/path', self.openImage)
        contr.addRecive("2d/tool", self.setTool)
        contr.addRecive("2d/image/off", self.updateImage)
        contr.addRecive("2d/image/location/x", self.set_x)
        contr.addRecive("2d/image/location/y", self.set_y)
        contr.addRecive("2d/image/scale/x", self.set_scale)
        contr.addSend("2d/image", self.imageChangeSig)
        contr.addSend("3d/model/path", self.modelChangePathSig)
        contr.addSend("3d/model/name", self.modelChangeNameSig)
        # contr.addSend("2d/image/path", self.imageChangePathSig)
        contr.addSend("2d/image/name", self.imageChangeNameSig)
        contr.addSend("2d/image/location/x/set", self.imageChangeLocX)
        contr.addSend("2d/image/location/y/set", self.imageChangeLocY)
        contr.addRecive('3d/view/top', self.addCameraImage)
        contr.addRecive("3d/bedSize", self.bedChanged)

        self.setAcceptDrops(True)
        self._zoom = 0
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)

        self.tool = None
        self.opacity = .5
        self.hidden = False

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(
            0, 0, sizeX, sizeY)
        # print(self.size())
        self.setAlignment(Qt.AlignBottom | Qt.AlignLeft)

        self.render = self.scene.addPixmap(QPixmap())
        self.texture = self.scene.addPixmap(QPixmap())
        self.setScene(self.scene)
        self.x = 0
        self.y = 0
        self.loadSettings()

    def drawBackground(self, painter, rect):
        background_brush = QBrush(QColor(153, 153, 153), Qt.SolidPattern)
        painter.fillRect(rect, background_brush)

    def loadSettings(self):
        settings = Settings()
        self._xBed = float(settings.printerSettings['bed_size_x'])
        self._yBed = float(settings.printerSettings['bed_size_y'])

    '''
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)
    '''

    def addCameraImage(self, image):
        if image.size().width() == 0:
            return
        # print("render size ->", image.size())
        image = image.scaled(
            550, 550, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        # image.save('test.png') #TODO
        self.render.setPixmap(image)
        self.scene.update()

    def set_x(self, x):
        # translation mm to px
        self.x = (550*x)/self._xBed
        print(self.x)
        self.updateCoord()

    def set_y(self, y):
        # translation mm to px
        self.y = -(550*y)//self._yBed
        self.updateCoord()

    def set_scale(self, scale):
        scale = scale/100
        self.scale = scale
        self.texture.setTransformOriginPoint(0, 550)
        self.texture.setScale(scale)
        #point = QPointF(0, (550-self.ph*scale))
        # self.texture.setOffset(point)
        # self.y = 550-self.texture.height()
        # self.scene.update()

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
        self.ph = pixmap.height()
        point = QPointF(0, 550-pixmap.height())
        self.texture.setOffset(point)
        self.texture.setPos(0, 0)
        self.x = 0
        self.y = 0
        self.texture.setZValue(1)  # TODO test
        self.texture.setOpacity(.5)
        if self.tool == 'move':
            self.texture.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.texture.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.imageChangeSig.emit(pixmap)

    def bedChanged(self, x, y):
        self._xBed = x
        self._yBed = y
        self.updateCoord()
        self.scene.update()

    def setOpacity(self, value):
        self.texture.setOpacity(value)
        self.opacity = value
        self.hidden = False

    def hideUnhide(self):
        if(self.hidden == True):
            self.texture.setOpacity(self.opacity)
            self.hidden = False
        else:
            self.texture.setOpacity(0)
            self.hidden = True

    def mouseMoveEvent(self, e):
        # conversion px to mm
        #self.x = (self.texture.scenePos().x()*self._xBed)/550
        #self.y = -(self.texture.scenePos().y()*self._yBed)//550
        self.imageChangeLocX.emit(
            (self.texture.scenePos().x()*self._xBed)/550)
        tmp = -((self.texture.scenePos().y()*self._yBed)//550)
        self.imageChangeLocY.emit(tmp)
        return super().mouseMoveEvent(e)

    def setTool(self, tool):
        if tool == 'move':
            self.texture.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.texture.setFlag(QGraphicsItem.ItemIsSelectable, True)
        elif tool == 'scale':
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
    iw = TEST_docking()
    # iw2 = ImageToolsWidget()
    Controller().match()
    # Controller().showConnections()
    iw.show()
    # iw2.show()
    sys.exit(app.exec_())
