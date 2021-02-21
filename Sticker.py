import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, x, y, on_top=False):
        super(Sticker, self).__init__()

        self.img_path = img_path
        self.x = x
        self.y = y
        self.on_top = on_top

        self.setupUi()
        self.show()

    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint if self.on_top else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        label.setMovie(movie)
        movie.start()

        self.setGeometry(
            self.x,
            self.y,
            movie.frameRect().size().width(),
            movie.frameRect().size().height()
        )

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    s1 = Sticker('gif/left.gif', x=-70, y=200, on_top=True)
    s2 = Sticker('gif/01.gif', x=500, y=500)
    
    sys.exit(app.exec_())
