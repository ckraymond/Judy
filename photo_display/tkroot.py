import time
import tkinter
import tkinter.font as tkfont
from PIL import Image, ImageTk

class tkRoot:

    def __init__(self):
        self.root = tkinter.Tk()
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.focus_set()
        self.root.attributes('-fullscreen', 1)
        self.root.config(cursor="none")

        #TODO: Need to check on this
        self.root.bind('t', self.talk_icon())

        # Now determine the canvas size
        self.canvas = tkinter.Canvas(self.root, width=self.w, height=self.h)
        self.canvas.pack()
        self.canvas.configure(background='black')

    def show_image(self, pilImage, photo_item, wait):
        # Code to show the image on the screen
        imgWidth, imgHeight = pilImage.size

        # resize photo to full screen
        ratio = min(self.w / imgWidth, self.h / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.LANCZOS)
        image = ImageTk.PhotoImage(pilImage)
        imagesprite = self.canvas.create_image(self.w / 2, self.h / 2, image=image)

        # Determine the correct width of the label (with a max)
        l_location = f'Location: {photo_item.location}'
        l_date = f'Date Taken: {photo_item.date}'
        l_people = f'People In Photo: {photo_item.people}'
        l_font = tkfont.Font(family = 'Arial Rounded MT Bold', size = 16, weight='normal')

        max_pxls = min(int(.4 * self.w),
                        max(l_font.measure(l_location),
                            l_font.measure(l_date),
                            l_font.measure(l_people)))
        l_width = max_pxls + 40


        # Add in a label with the image info
        label = tkinter.Label(self.root,
                              text=f'{l_location}\n{l_date}\n{l_people}',
                              font=l_font,
                              bg='white',
                              fg='#001455',
                              justify=tkinter.RIGHT)
        label.place(x=self.w - l_width-20, y=self.h - 90, width = l_width, height=70)

        self.root.update_idletasks()
        self.root.update()

        self.talk_icon()

        time.sleep(wait)

    def talk_icon(self):
        logo_image = Image.open('data/judy_logo.png')
        logo_image = logo_image.resize((50, 50), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_image)

        logo_panel = tkinter.Label(self.root)
        logo_panel.image = logo_image
        logo_panel.place(x=20, y=40, width=50, height=50)



