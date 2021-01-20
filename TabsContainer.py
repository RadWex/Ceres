from PySide2.QtWidgets import (QWidget, QVBoxLayout,
                               QTabWidget, QPushButton,
                               QLabel, QPlainTextEdit)
from SettingsWindow import SettingsWindow
from Settings import Settings
from ModelManipulation import ModelManipulation
from ImageManipulation import ImageManipulation


class TabContainerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(350)
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tab1 = ModelManipulation()
        self.tab2 = ImageManipulation()
        self.tab3 = QWidget()
        self.tab4 = GcodeSettings()

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.tabs.addTab(self.tab1, "Model")
        self.tabs.addTab(self.tab2, "Image")
        self.tabs.addTab(self.tab3, "Engraving")
        self.tabs.addTab(self.tab4, "G-code")

        self.layout.addWidget(self.tabs)
        self.processBtn = QPushButton("Process")
        self.layout.addWidget(self.processBtn)
        self.exportBtn = QPushButton("Export G-code")
        self.exportBtn.setEnabled(False)
        self.layout.addWidget(self.exportBtn)
        self.setLayout(self.layout)


class GcodeSettings(QWidget):
    def __init__(self):
        super().__init__()
        horizontalLayout = QVBoxLayout()
        self.setLayout(horizontalLayout)

        settings = Settings()
        horizontalLayout.addWidget(QLabel("Start G-code"))
        gcodeTextEditStart = QPlainTextEdit()
        gcodeTextEditStart.insertPlainText(settings.gcode["start"])
        horizontalLayout.addWidget(gcodeTextEditStart)

        horizontalLayout.addWidget(QLabel("End G-code"))
        gcodeTextEditEnd = QPlainTextEdit()
        gcodeTextEditEnd.insertPlainText(settings.gcode["end"])
        horizontalLayout.addWidget(gcodeTextEditEnd)
