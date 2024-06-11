import tkinter                                              # Used for all grpahics on the device
from PIL import Image, ImageTk
from photo_display.photo_display import photoDisplay        # Used to actually display the photos

class judyMVP:

    def __init__(self):
        tk_screen = tkRoot()
        photo_display = photoDisplay(tk_screen)



class tkRoot:

    def __init__(self):
        self.root = tkinter.Tk()
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.focus_set()
        self.canvas = tkinter.Canvas(self.root, width=self.w, height=self.h)
        self.canvas.pack()
        self.canvas.configure(background='black')

    def show_image(self, pilImage):
        imgWidth, imgHeight = pilImage.size
        # resize photo to full screen
        ratio = min(self.w / imgWidth, self.h / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.LANCZOS)
        image = ImageTk.PhotoImage(pilImage)
        imagesprite = self.canvas.create_image(self.w / 2, self.h / 2, image=image)
        self.root.update_idletasks()
        self.root.update()
