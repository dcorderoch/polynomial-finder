from image_viewer import *

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap

import os
import sys


class My_Application(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.checkPath)

        self.sceneRef = QObject()
        self.num = 0
        self.checkPath()

    def checkPath(self):
        self.num += 1
        if self.num > 3:
            self.num = 1
        image_path = 'image' + str(self.num) + '.png'
        if os.path.isfile(image_path):
            print(f'can show!')
            scene = QtWidgets.QGraphicsScene(self)
            pixmap = QPixmap(image_path)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            self.ui.graphicsView.setScene(scene)
            self.sceneRef.deleteLater()
            self.sceneRef = scene


if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_instance = My_Application()
    class_instance.show()
    sys.exit(app.exec_())
