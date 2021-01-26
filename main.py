import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QLocale
from MainWindow import MainWindow
from Controller import Controller


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QLocale.setDefault(QLocale(QLocale.English))
    mainWindow = MainWindow()
    Controller().match()
    mainWindow.show()
    mainWindow.centerOnScreen()
    sys.exit(app.exec_())
