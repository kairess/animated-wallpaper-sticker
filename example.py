from tkinter import *
from pyscreenshot import grab
from PIL import ImageTk, Image

X, Y = 100, 100
SPEED = 25

fg_img = Image.open('gif/left.gif')

n_frames = fg_img.n_frames
w, h = fg_img.size

bg_img = grab(bbox=(X, Y, X+w, Y+h))
bg_img = bg_img.resize((w, h))
bg_img = bg_img.convert('RGBA')

root = Tk()
# root.wm_attributes('-topmost', True)
root.overrideredirect(True)
root.geometry(f'+{X}+{Y}')


frames = []
for i in range(n_frames):
    fg_img.seek(i)

    frame = fg_img.convert('RGBA')
    frame = Image.alpha_composite(bg_img, frame)
    frame = ImageTk.PhotoImage(frame)

    frames.append(frame)


def update(index):
    frame = frames[index]

    label.config(image=frame)

    index += 1
    if index == n_frames:
        index = 0

    root.after(SPEED, update, index)


label = Label(root, borderwidth=0)
label.pack()
root.after(0, update, 0)

root.mainloop()
