from screeninfo import get_monitors
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie
import random, sys

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()
        self.timer = QtCore.QTimer(self)
        self.img_path = img_path
        self.xy = xy
        self.from_xy = xy
        self.from_xy_diff = [0, 0]
        self.to_xy = xy
        self.to_xy_diff = [0, 0]
        self.speed = 60
        self.direction = [0, 0] # x: 0(left), 1(right), y: 0(up), 1(down)
        self.size = size
        self.on_top = on_top
        self.localPos = None
        self.health = 100

        self.setupUi()
        self.show()

    def walk(self, from_xy, to_xy, speed=60):
        self.from_xy = from_xy
        self.to_xy = to_xy
        self.speed = speed

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.__walkHandler)
        self.timer.start(1000 / self.speed)

    # 초기 위치로부터의 상대적 거리를 이용한 walk
    def walk_diff(self, from_xy_diff, to_xy_diff, speed=60, restart=False):
        self.from_xy_diff = from_xy_diff
        self.to_xy_diff = to_xy_diff
        self.from_xy = [self.xy[0] + self.from_xy_diff[0], self.xy[1] + self.from_xy_diff[1]]
        self.to_xy = [self.xy[0] + self.to_xy_diff[0], self.xy[1] + self.to_xy_diff[1]]
        self.speed = speed
        if restart:
            self.timer.start()
        else:
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
        layout = QtWidgets.QVBoxLayout(centralWidget)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint if self.on_top else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        label = QtWidgets.QLabel()
        movie = QMovie(self.img_path)
        label.setMovie(movie)
        movie.start()
        movie.stop()

        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()

        self.setGeometry(self.xy[0], self.xy[1], w, h)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setStyleSheet('QProgressBar::chunk { background: red; } QProgressBar { text-align: center; }')
        self.progress.setMaximum(self.health)
        self.progress.setValue(self.health)

        layout.addWidget(label)
        layout.addWidget(self.progress)

    def mousePressEvent(self, e):
        self.health -= 10
        self.progress.setValue(self.health)

        if self.health <= 0:
            self.destroy()


if __name__ == '__main__':
    MAX_STICKERS = 30
    MAX_MOVES = 200

    app = QtWidgets.QApplication(sys.argv)

    monitor = get_monitors()[0]
    screen_w = monitor.width
    screen_h = monitor.height

    stickers = []

    for i in range(MAX_STICKERS):
        s = Sticker(
            'gif/bug.gif',
            xy=[random.randint(0, screen_w), random.randint(0, screen_h)],
            size=random.randint(50, 100) / 100,
            on_top=True
        )

        s.walk_diff(
            from_xy_diff=[random.randint(-MAX_MOVES, MAX_MOVES), random.randint(-MAX_MOVES, MAX_MOVES)],
            to_xy_diff=[random.randint(-MAX_MOVES, MAX_MOVES), random.randint(-MAX_MOVES, MAX_MOVES)]
        )

        stickers.append(s)

    sys.exit(app.exec_())
