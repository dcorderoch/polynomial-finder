from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(771, 569)

        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(25, 53, 721, 491))
        self.graphicsView.setSizeIncrement(QtCore.QSize(0, 0))
        self.graphicsView.setFrameShadow(QtWidgets.QFrame.Raised)
        self.graphicsView.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.graphicsView.setAlignment(
            QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.graphicsView.setObjectName("graphicsView")

        self.startBtn = QtWidgets.QPushButton(Dialog)
        self.startBtn.setGeometry(QtCore.QRect(670, 15, 75, 23))
        self.startBtn.setObjectName("pushBtn")

        self.stopBtn = QtWidgets.QPushButton(Dialog)
        self.stopBtn.setGeometry(QtCore.QRect(595, 15, 75, 23))
        self.stopBtn.setObjectName("stopBtn")

        self.quitBtn = QtWidgets.QPushButton(Dialog)
        self.quitBtn.setGeometry(QtCore.QRect(25, 15, 75, 23))
        self.quitBtn.setObjectName("rstBtn")

        self.rstBtn = QtWidgets.QPushButton(Dialog)
        self.rstBtn.setGeometry(QtCore.QRect(190, 15, 75, 23))
        self.rstBtn.setObjectName("rstBtn")

        self.f1Btn = QtWidgets.QPushButton(Dialog)
        self.f1Btn.setGeometry(QtCore.QRect(370, 15, 75, 23))
        self.f1Btn.setObjectName("f1Btn")

        self.f2Btn = QtWidgets.QPushButton(Dialog)
        self.f2Btn.setGeometry(QtCore.QRect(445, 15, 75, 23))
        self.f2Btn.setObjectName("f2Btn")

        self.f3Btn = QtWidgets.QPushButton(Dialog)
        self.f3Btn.setGeometry(QtCore.QRect(520, 15, 75, 23))
        self.f3Btn.setObjectName("f3Btn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Image Viewer"))
        self.startBtn.setText(_translate("Dialog", "start"))
        self.stopBtn.setText(_translate("Dialog", "stop"))
        self.f1Btn.setText(_translate("Dialog", "f1"))
        self.f2Btn.setText(_translate("Dialog", "f2"))
        self.f3Btn.setText(_translate("Dialog", "f3"))
        self.rstBtn.setText(_translate("Dialog", "reset"))
        self.quitBtn.setText(_translate("Dialog", "quit"))
