import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'show image'
        self.left = 10
        self.top = 10
        self.width = 480
        self.height = 270
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        label = QLabel(self)
        pixmap = QPixmap('plot.png')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
