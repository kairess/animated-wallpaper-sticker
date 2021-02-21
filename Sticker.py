import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()

        self.img_path = img_path
        self.xy = xy
        self.from_xy = xy
        self.to_xy = xy
        self.speed = 60
        self.direction = [0, 0] # x: 0(left), 1(right), y: 0(up), 1(down)
        self.size = size
        self.on_top = on_top

        self.setupUi()
        self.show()

    def walk(self, from_xy, to_xy, speed=60):
        self.from_xy = from_xy
        self.to_xy = to_xy
        self.speed = speed

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.__walkHandler)
        self.timer.start(1000 / self.speed)

    def __walkHandler(self):
        if self.xy[0] >= self.to_xy[0]:
            self.direction[0] = 0
        elif self.xy[0] < self.from_xy[0]:
            self.direction[0] = 1

        if self.direction[0] == 0:
            self.xy[0] -= 1
        else:
            self.xy[0] += 1

        if self.xy[1] >= self.to_xy[1]:
            self.direction[1] = 0
        elif self.xy[1] < self.from_xy[1]:
            self.direction[1] = 1

        if self.direction[1] == 0:
            self.xy[1] -= 1
        else:
            self.xy[1] += 1

        self.move(*self.xy)

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

        self.setGeometry(self.xy[0], self.xy[1], w, h)

    def mouseDoubleClickEvent(self, e):
        QtWidgets.qApp.quit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    s = Sticker('gif/left.gif', xy=[-80, 200], on_top=False)

    s1 = Sticker('gif/amongus/red_vent.gif', xy=[780, 1020], size=0.3, on_top=True)

    s2 = Sticker('gif/amongus/orange.gif', xy=[1200, 1020], size=0.3, on_top=True)
    s2.walk(from_xy=[1200, 1010], to_xy=[1220, 1020])

    s3 = Sticker('gif/amongus/blue_green.gif', xy=[400, 920], size=1.0, on_top=True)

    s4 = Sticker('gif/amongus/mint.gif', xy=[1000, 950], size=0.2, on_top=True)
    s4.walk(from_xy=[900, 950], to_xy=[1100, 950], speed=120)

    s5 = Sticker('gif/amongus/brown.gif', xy=[200, 1010], size=0.75, on_top=True)

    s6 = Sticker('gif/amongus/yellow.gif', xy=[1850, 800], size=0.75, on_top=True)
    # s6.walk(from_xy=[0, 800], to_xy=[1850, 800], speed=240)

    s7 = Sticker('gif/amongus/magenta.gif', xy=[1500, 900], size=0.5, on_top=True)
    s7.walk(from_xy=[1400, 900], to_xy=[1600, 900], speed=180)

    sys.exit(app.exec_())
