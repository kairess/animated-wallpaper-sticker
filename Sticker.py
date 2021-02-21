from tkinter import *
from pyscreenshot import grab
from PIL import ImageTk, Image

class Sticker():
    def __init__(self, img_path, x, y, speed=25):
        self.x = x
        self.y = y
        self.speed = speed

        self.load_gif(img_path)
        self.screenshot()

    # https://stackoverflow.com/questions/61958291/gifs-read-with-pillow-have-black-borders
    def load_gif(self, img_path):
        img = Image.open(img_path)
        self.w, self.h = img.size

        self.frames = []

        disposal_method_last = 0

        try:
            while True:
                disposal_method = disposal_method_last
                disposal_method_last = img.__dict__.get('disposal_method', 0)

                if disposal_method == 2 or (disposal_method == 1 and self.frames == []):
                    frame = Image.new('RGBA', img.size, color=(255, 0, 0, 0))
                    frame.paste(img.crop(img.dispose_extent), box=(img.dispose_extent[0], img.dispose_extent[1]))
                elif disposal_method == 1:
                    newStuff = img.crop(img.dispose_extent)
                    frame = self.frames[-1].copy()
                    frame.paste(newStuff, img.dispose_extent, newStuff.convert("RGBA"))
                else:
                    frame = img.copy()

                frame = frame.convert('RGBA')
                self.frames.append(frame)
                img.seek(img.tell() + 1)
        except EOFError:
            pass

    def screenshot(self):
        self.bg_img = grab(bbox=(self.x, self.y, self.x + self.w, self.y + self.h))
        self.bg_img = self.bg_img.resize((self.w, self.h))
        self.bg_img = self.bg_img.convert('RGBA')

    def build(self, root):
        window = Toplevel(root)
        window.geometry(f'+{self.x}+{self.y}')
        window.overrideredirect(True)

        frames_tk = []
        for frame in self.frames:
            frame = Image.alpha_composite(self.bg_img, frame)
            frame = ImageTk.PhotoImage(frame)
            frames_tk.append(frame)

        def update(index):
            frame = frames_tk[index]

            label.config(image=frame)

            index += 1
            if index == len(self.frames):
                index = 0

            window.after(self.speed, update, index)

        label = Label(window, borderwidth=0)
        label.pack()
        window.after(0, update, 0)

root = Tk()
root.overrideredirect(True)
root.withdraw()

sticker1 = Sticker('gif/01.gif', x=500, y=200, speed=25)
sticker1.build(root)

sticker2 = Sticker('gif/left.gif', x=0, y=100, speed=25)
sticker2.build(root)

root.mainloop()