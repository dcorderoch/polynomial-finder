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
    resetting = pyqtSignal()

    function = -1

    def enable_start_btn(self, index):
        self.ui.pushButton.setDisabled(False)
        self.worker.set_data(index)
        self.ui.f0Button.setDisabled(True)
        self.ui.f1Button.setDisabled(True)
        self.ui.f2Button.setDisabled(True)
        self.ui.f3Button.setDisabled(True)
        self.function = index

    def enable_stop(self):
        self.ui.pushButton.setDisabled(True)
        self.ui.stopButton.setDisabled(False)

    def reset(self):
        self.ui.f0Button.setDisabled(False)
        self.ui.f1Button.setDisabled(False)
        self.ui.f2Button.setDisabled(False)
        self.ui.f3Button.setDisabled(False)
        self.ui.pushButton.setDisabled(False)
        self.ui.stopButton.setDisabled(True)
        self.resetting.emit()

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
        self.ui.pushButton.clicked.connect(self.enable_stop)
        self.ui.stopButton.clicked.connect(self.worker.finish)
        self.ui.stopButton.clicked.connect(
            lambda: self.ui.stopButton.setDisabled(True))
        self.ui.stopButton.clicked.connect(
            lambda: self.ui.resetButton.setDisabled(False))
        self.ui.f0Button.clicked.connect(lambda: self.enable_start_btn(0))
        self.ui.f1Button.clicked.connect(lambda: self.enable_start_btn(1))
        self.ui.f2Button.clicked.connect(lambda: self.enable_start_btn(2))
        self.ui.f3Button.clicked.connect(lambda: self.enable_start_btn(3))
        self.ui.resetButton.clicked.connect(self.reset)
        self.ui.resetButton.clicked.connect(
            lambda: self.ui.resetButton.setDisabled(True))
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
        """
        Polinomials is a tuple of 5 p polinomials, and each p the coefficients of the polinomial
        """
        lowest = 1000
        highest = -1000

        f_x = (*(x[0] for x in f_data),)
        f_y = (*(x[1] for x in f_data),)

        for x in f_x:
            if x < lowest:
                lowest = x
            if x > highest:
                highest = x

        x_start = lowest  # change this, use the smallest X in the data
        x_end = highest  # change this, use the biggest X in the data
        slices = len(f_x)  # smooth the curve
        x = linspace(x_start, x_end, slices)

        plt.plot(f_x, f_y, color='black')

        colors = ('#0000CC', '#0088FF', '#00CC00', '#CC8800', '#FF0000')

        for i, p in enumerate(Polinomials):
            ys = ()
            for x in f_x:
                y = 0
                for j, coeff in enumerate(p):
                    y += coeff * x ** j
                ys = (*ys, y)
            plt.plot(f_x, ys, color=colors[i], label=f'rank {i+1}')

        image_path = f'generation.png'

        plt.title(f'function: {self.function} - generation: {generation}')
        plt.legend()

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
