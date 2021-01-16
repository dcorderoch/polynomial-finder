from genal import genal

from image_viewer import *

from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QMainWindow

from numpy import linspace, sin, cos  # gotta change this
import math  # for the pi thing
import matplotlib.pyplot as plt

import os
import sys

"""
steps:
    start a generation
    calculate population's fitness
    select mating pool
    do crossover
    check if going to mutate
    do mutation
    kill the weak ones
    check the fitness against confidence level/error
    if candidate is a chad, or too many generations, finish
"""


class PolyFinderGUI(QMainWindow):
    updated = pyqtSignal()

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
        self.ui.pushButton.clicked.connect(self.worker.initialize)
        self.updated.connect(self.worker.start_crunching)

        self.sceneRef = QObject()

        self.show()

    def graph(self, x, coeffs):
        y = 0
        for i, c in enumerate(coeffs):
            y += c * x ** i
        return y

    def update_graph(self, Polinomials, generation):
        """
        Polinomials is a tuple of 5 p polinomials, and each p the coefficients of the polinomial
        """
        x_start = 0  # change this, use the smallest X in the data
        x_end = 10  # change this, use the biggest X in the data
        slices = 1000  # smooth the curve
        x = linspace(x_start, x_end, slices)

        # need exactly 5 colors for the individuals
        colors = ('blue', 'green', 'yellow', 'orange', 'red')

        for i in range(len(colors)):
            plt.plot(x, self.graph(x, Polinomials[i]))

        image_path = f'generation.png'

        plt.savefig(image_path)
        plt.clf()

        scene = QGraphicsScene(self)
        pixmap = QPixmap(image_path)
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.ui.graphicsView.setScene(scene)
        self.sceneRef.deleteLater()
        self.sceneRef = scene
        QTimer.singleShot(0, lambda: self.updated.emit())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_instance = PolyFinderGUI()
    class_instance.show()
    sys.exit(app.exec_())
