from Sticker2 import Sticker
from screeninfo import get_monitors
from PyQt5 import QtCore, QtWidgets, QtGui
import random, sys

MAX_STICKERS = 10
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