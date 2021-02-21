import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, x, y, size=1.0, on_top=False):
        super(Sticker, self).__init__()

        self.img_path = img_path
        self.x = x
        self.y = y
        self.size = size
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
        movie.stop()

        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()

        self.setGeometry(self.x, self.y, w, h)

    def mouseDoubleClickEvent(self, e):
        QtWidgets.qApp.quit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    s = Sticker('gif/left.gif', x=-80, y=200, on_top=False)

    s1 = Sticker('gif/amongus/red_vent.gif', x=780, y=1020, size=0.3, on_top=True)
    s2 = Sticker('gif/amongus/orange.gif', x=1200, y=1020, size=0.3, on_top=True)
    s3 = Sticker('gif/amongus/blue_green.gif', x=400, y=920, size=1.0, on_top=True)
    s4 = Sticker('gif/amongus/mint.gif', x=1000, y=950, size=0.2, on_top=True)
    s5 = Sticker('gif/amongus/brown.gif', x=200, y=1010, size=0.75, on_top=True)
    s6 = Sticker('gif/amongus/yellow.gif', x=1850, y=800, size=0.75, on_top=True)
    s7 = Sticker('gif/amongus/magenta.gif', x=1500, y=900, size=0.5, on_top=True)

    sys.exit(app.exec_())
