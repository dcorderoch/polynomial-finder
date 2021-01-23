from genal import genal

from image_viewer import *

from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage

from PyQt5.QtWidgets import QMainWindow

from numpy import linspace, sin, cos  # gotta change this
import math  # for the pi thing
import matplotlib.pyplot as plt

import os
import sys
import io


class PolyFinderGUI(QMainWindow):
    updated = pyqtSignal()
    resetting = pyqtSignal()

    function = -1

    def enable_start_btn(self, index):
        self.ui.pushBtn.setDisabled(False)
        self.worker.set_data(index)
        self.ui.f1Btn.setDisabled(True)
        self.ui.f2Btn.setDisabled(True)
        self.ui.f3Btn.setDisabled(True)
        self.function = index

    def enable_stop(self):
        self.ui.pushBtn.setDisabled(True)
        self.ui.stopBtn.setDisabled(False)

    def reset(self):
        self.ui.f1Btn.setDisabled(False)
        self.ui.f2Btn.setDisabled(False)
        self.ui.f3Btn.setDisabled(False)
        self.ui.stopBtn.setDisabled(True)
        self.resetting.emit()

    def on_stop_btn(self):
        self.ui.stopBtn.setDisabled(True)
        self.ui.rstBtn.setDisabled(False)
        self.ui.quitBtn.setDisabled(False)

    def on_rst_btn(self):
        self.reset()
        self.ui.rstBtn.setDisabled(True)
        self.ui.quitBtn.setDisabled(True)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.worker = genal.PolyFinder()
        self.worker_thread = QThread()

        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self.worker.generated.connect(self.update_graph)
        self.worker.initialized.connect(self.worker.start_crunching)
        self.worker.finished.connect(lambda: self.on_stop_btn())
        self.ui.pushBtn.clicked.connect(self.worker.initialize)
        self.ui.pushBtn.clicked.connect(self.enable_stop)
        self.ui.stopBtn.clicked.connect(self.worker.finish)
        self.ui.stopBtn.clicked.connect(lambda: self.on_stop_btn())
        self.ui.f1Btn.clicked.connect(lambda: self.enable_start_btn(1))
        self.ui.f2Btn.clicked.connect(lambda: self.enable_start_btn(2))
        self.ui.f3Btn.clicked.connect(lambda: self.enable_start_btn(3))
        self.ui.rstBtn.clicked.connect(lambda: self.on_rst_btn())
        self.ui.quitBtn.clicked.connect(lambda: QApplication.quit())
        self.resetting.connect(self.worker.reset)
        self.updated.connect(self.worker.start_crunching)

        self.sceneRef = QObject()

        self.show()

    def graph(self, x, coeffs):
        y = 0
        for i, c in enumerate(coeffs):
            y += c * x ** i
        return y

    def update_graph(self, Polinomials, f_data, generation):
        f_x = (*(x[0] for x in f_data),)
        f_y = (*(x[1] for x in f_data),)

        plt.plot(f_x, f_y, color='black')

        colors = ('#0000CC', '#0088FF', '#00CC00', '#CC8800', '#FF0000')

        for i, p in enumerate(Polinomials):
            f_f = (*(genal.polimerize(x, p) for x in f_x),)
            plt.plot(f_x, f_f, label=f'rank {i+1}')

        plt.title(f'function: {self.function} - generation: {generation}')
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf)
        plt.clf()
        scene = QGraphicsScene(self)
        item = QGraphicsPixmapItem(
            QPixmap.fromImage(
                QImage.fromData(
                    buf.getbuffer())))
        scene.addItem(item)
        self.ui.graphicsView.setScene(scene)

        self.sceneRef.deleteLater()
        self.sceneRef = scene
        self.updated.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_instance = PolyFinderGUI()
    class_instance.show()
    sys.exit(app.exec_())
