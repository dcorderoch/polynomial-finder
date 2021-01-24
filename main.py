from genal import genal

from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGridLayout,
    QPushButton,
    QWidget
)
from PyQt5.QtGui import QPixmap, QImage

from PyQt5.QtWidgets import QMainWindow

from numpy import linspace, sin, cos  # gotta change this
import math  # for the pi thing

import os
import sys
import io

import numpy as np
import pyqtgraph as pg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class PolyFinderGUI(QMainWindow):
    updated = pyqtSignal()
    resetting = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.startBtn = QPushButton()
        self.stopBtn = QPushButton()
        self.quitBtn = QPushButton()
        self.rstBtn = QPushButton()
        self.f1Btn = QPushButton()
        self.f2Btn = QPushButton()
        self.f3Btn = QPushButton()

        self.setup_ui()

        self.worker = genal.PolyFinder()
        self.worker_thread = QThread()

        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self.make_signal_connections()

        #self.sceneRef = QObject()

        self.widget = QWidget()
        self.plot_widget = pg.PlotWidget()

        self.curve0 = pg.PlotDataItem()
        self.curve1 = pg.PlotDataItem()
        self.curve2 = pg.PlotDataItem()
        self.curve3 = pg.PlotDataItem()
        self.curve4 = pg.PlotDataItem()
        self.curve5 = pg.PlotDataItem()

        self.plot_widget.addItem(self.curve0)
        self.plot_widget.addItem(self.curve1)
        self.plot_widget.addItem(self.curve2)
        self.plot_widget.addItem(self.curve3)
        self.plot_widget.addItem(self.curve4)
        self.plot_widget.addItem(self.curve5)

        layout = QGridLayout()

        self.widget.setLayout(layout)

        # (widget, row, column)
        layout.addWidget(self.startBtn, 0, 0)
        layout.addWidget(self.stopBtn, 0, 1)
        layout.addWidget(self.quitBtn, 0, 2)
        layout.addWidget(self.rstBtn, 0, 3)
        layout.addWidget(self.f1Btn, 0, 4)
        layout.addWidget(self.f2Btn, 0, 5)
        layout.addWidget(self.f3Btn, 0, 6)

        # (widget, fromRow, fromCol, rowSpan, colSpan)
        layout.addWidget(self.plot_widget, 1, 0, 2, 7)

        self.setCentralWidget(self.widget)

        self.show()

    def make_signal_connections(self):
        self.worker.generated.connect(self.update_graph)
        self.worker.initialized.connect(self.worker.start_crunching)
        self.worker.finished.connect(lambda: self.on_stop_btn())
        self.startBtn.clicked.connect(self.worker.initialize)
        self.startBtn.clicked.connect(self.enable_stop)
        self.stopBtn.clicked.connect(self.worker.finish)
        self.stopBtn.clicked.connect(lambda: self.on_stop_btn())
        self.f1Btn.clicked.connect(lambda: self.enable_start_btn(1))
        self.f2Btn.clicked.connect(lambda: self.enable_start_btn(2))
        self.f3Btn.clicked.connect(lambda: self.enable_start_btn(3))
        self.rstBtn.clicked.connect(lambda: self.on_rst_btn())
        self.quitBtn.clicked.connect(lambda: QApplication.quit())
        self.resetting.connect(self.worker.reset)
        self.updated.connect(self.worker.start_crunching)

    def setup_ui(self):
        self.startBtn.setText("start")
        self.startBtn.setMinimumWidth(75)
        self.stopBtn.setText("stop")
        self.stopBtn.setMinimumWidth(75)
        self.quitBtn.setText("quit")
        self.quitBtn.setMinimumWidth(75)
        self.rstBtn.setText("reset")
        self.rstBtn.setMinimumWidth(75)
        self.f1Btn.setText("f1")
        self.f1Btn.setMinimumWidth(75)
        self.f2Btn.setText("f2")
        self.f2Btn.setMinimumWidth(75)
        self.f3Btn.setText("f3")
        self.f3Btn.setMinimumWidth(75)

        self.startBtn.setDisabled(True)
        self.stopBtn.setDisabled(True)
        self.rstBtn.setDisabled(True)

    def enable_start_btn(self, index):
        self.startBtn.setDisabled(False)
        self.worker.set_data(index)
        self.f1Btn.setDisabled(True)
        self.f2Btn.setDisabled(True)
        self.f3Btn.setDisabled(True)
        self.quitBtn.setDisabled(True)

    def enable_stop(self):
        self.startBtn.setDisabled(True)
        self.stopBtn.setDisabled(False)

    def reset(self):
        self.f1Btn.setDisabled(False)
        self.f2Btn.setDisabled(False)
        self.f3Btn.setDisabled(False)
        self.stopBtn.setDisabled(True)
        self.resetting.emit()

    def on_stop_btn(self):
        self.stopBtn.setDisabled(True)
        self.rstBtn.setDisabled(False)
        self.quitBtn.setDisabled(False)

    def on_rst_btn(self):
        self.reset()
        self.rstBtn.setDisabled(True)

    def graph(self, x, coeffs):
        y = 0
        for i, c in enumerate(coeffs):
            y += c * x ** i
        return y

    def update_graph(self, Polinomials, f_data, generation):
        f_x = (*(x[0] for x in f_data),)
        f_y = (*(x[1] for x in f_data),)

        f_f0 = f_y
        self.curve0.setPen(color=(0, 0, 0), width=6, name='raw')
        self.curve0.setData([*f_x, ], [*f_f0, ])

        # colors = ('#0000CC', '#0088FF', '#00CC00', '#CC8800', '#FF0000')
        colors = ((0, 0, 204), (0, 136, 255),
                  (0, 204, 0), (204, 136, 0), (255, 0, 0))

        f_f1 = (*(genal.polimerize(x, Polinomials[0]) for x in f_x),)
        self.curve1.setPen(color=colors[0], width=4, name='rank 1')
        self.curve1.setData([*f_x, ], [*f_f1, ])
        f_f2 = (*(genal.polimerize(x, Polinomials[1]) for x in f_x),)
        self.curve2.setPen(color=colors[1], width=2, name='rank 2')
        self.curve2.setData([*f_x, ], [*f_f2, ])
        f_f3 = (*(genal.polimerize(x, Polinomials[2]) for x in f_x),)
        self.curve3.setPen(color=colors[2], width=2, name='rank 3')
        self.curve3.setData([*f_x, ], [*f_f3, ])
        f_f4 = (*(genal.polimerize(x, Polinomials[3]) for x in f_x),)
        self.curve4.setPen(color=colors[3], width=2, name='rank 4')
        self.curve4.setData([*f_x, ], [*f_f4, ])
        f_f5 = (*(genal.polimerize(x, Polinomials[4]) for x in f_x),)
        self.curve5.setPen(color=colors[4], width=2, name='rank 5')
        self.curve5.setData([*f_x, ], [*f_f5, ])

        self.updated.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_instance = PolyFinderGUI()
    class_instance.show()
    sys.exit(app.exec_())
