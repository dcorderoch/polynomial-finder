from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(766, 569)
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(25, 71, 721, 491))
        self.graphicsView.setSizeIncrement(QtCore.QSize(0, 0))
        self.graphicsView.setFrameShadow(QtWidgets.QFrame.Raised)
        self.graphicsView.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.graphicsView.setAlignment(
            QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.graphicsView.setObjectName("graphicsView")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(670, 40, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setDisabled(True)

        self.stopButton = QtWidgets.QPushButton(Dialog)
        self.stopButton.setGeometry(QtCore.QRect(595, 40, 75, 23))
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setDisabled(True)

        self.f0Button = QtWidgets.QPushButton(Dialog)
        self.f0Button.setGeometry(QtCore.QRect(520, 40, 75, 23))
        self.f0Button.setObjectName("f0Button")

        self.f1Button = QtWidgets.QPushButton(Dialog)
        self.f1Button.setGeometry(QtCore.QRect(445, 40, 75, 23))
        self.f1Button.setObjectName("f1Button")

        self.f2Button = QtWidgets.QPushButton(Dialog)
        self.f2Button.setGeometry(QtCore.QRect(370, 40, 75, 23))
        self.f2Button.setObjectName("f2Button")

        self.f3Button = QtWidgets.QPushButton(Dialog)
        self.f3Button.setGeometry(QtCore.QRect(295, 40, 75, 23))
        self.f3Button.setObjectName("f3Button")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Image Viewer"))
        self.pushButton.setText(_translate("Dialog", "start"))
        self.stopButton.setText(_translate("Dialog", "stop"))
        self.f0Button.setText(_translate("Dialog", "f0"))
        self.f1Button.setText(_translate("Dialog", "f1"))
        self.f2Button.setText(_translate("Dialog", "f2"))
        self.f3Button.setText(_translate("Dialog", "f3"))
