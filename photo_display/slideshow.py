import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import time
import logging

# Import other classes from Judy photo slideshow
from .photocanvas import photoCanvas
from .imagebackground import imageBackground

class slideShow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(1)
        self.root.title('Judy v0.1')
        self.root.geometry("%dx%d+0+0" % (self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")

        # Create blank canvas
        self.photo_canvas = photoCanvas(self.root)

        # Bind the keys for now
        self.root.bind('<KeyPress>', lambda event: self.show_mic_label(event))
        self.root.bind('<KeyRelease>', lambda event: self.hide_mic_label(event))

    def show_mic_label(self, event):
        '''
        Creates a new mic label.
        :param event:
        :param canvas:
        :return:
        '''
        logging.info(event)
        print(event)
        self.mic_oval = self.photo_canvas.canvas.create_oval(20, 20, 90, 90, fill='#FFFFFF')

        mic_image = ImageTk.PhotoImage(Image.open('data/judy_logo.png').resize((45, 45)))
        self.mic_image = self.photo_canvas.canvas.create_image(55, 55, image=mic_image)
        self.root.update_idletasks()
        self.root.update()

    def hide_mic_label(self, event):
        '''
        Deletes existing mic label.
        :param event:
        :param canvas:
        :return:
        '''
        logging.info(event)
        print(event)
        self.photo_canvas.canvas.delete(self.mic_image)
        self.photo_canvas.canvas.delete(self.mic_oval)
        self.root.update_idletasks()
        self.root.update()

    def set_background(self, image, photo_item, delay):
        '''
        Updates the canvas with the image as well as the image information.
        :param image:
        :param photo_item:
        :return:
        '''

        print('Updating image')
        self.image_background = imageBackground(image, self.photo_canvas.canvas, self.root)
        # self.image_label = imageLabel(self.photo_canvas.canvas, self.root)

        self.root.update()
        time.sleep(delay)

    #     # Now determine the canvas size
    #     self.canvas = tkinter.Canvas(self.root, width=self.w, height=self.h)
    #     self.canvas.configure(background='black')
    #     self.canvas.pack()
    #
    #     self.talk_icon()
    #
    # def show_image(self, pilImage, photo_item):
    #     # Code to show the image on the screen
    #     imgWidth, imgHeight = pilImage.size
    #
    #     # resize photo to full screen
    #     ratio = min(self.w / imgWidth, self.h / imgHeight)
    #     imgWidth = int(imgWidth * ratio)
    #     imgHeight = int(imgHeight * ratio)
    #     pilImage = pilImage.resize((imgWidth, imgHeight), Image.LANCZOS)
    #     image = ImageTk.PhotoImage(pilImage)
    #     self.main_image = self.canvas.create_image(self.w / 2, self.h / 2, image=image)
    #
    #     self.draw_label(photo_item)
    #
    #     self.root.bind('<Key-Return>', self.show_logo)
    #     self.root.bind('<KeyRelease>', self.hide_logo)
    #     self.root.focus_set()
    #     self.root.update_idletasks()
    #     self.root.update()
    #
    # def draw_label(self, photo_item):
    #     # Determine the correct width of the label (with a max)
    #     l_location = f'Location: {photo_item.location}'
    #     l_date = f'Date Taken: {photo_item.date}'
    #     l_people = f'People In Photo: {photo_item.people}'
    #     l_font = tkfont.Font(family = 'Arial Rounded MT Bold', size = 16, weight='normal')
    #
    #     max_pxls = min(int(.4 * self.w),
    #                     max(l_font.measure(l_location),
    #                         l_font.measure(l_date),
    #                         l_font.measure(l_people)))
    #     l_width = max_pxls + 40
    #
    #
    #     # Add in a label with the image info
    #     label = tkinter.Label(self.root,
    #                           text=f'{l_location}\n{l_date}\n{l_people}',
    #                           font=l_font,
    #                           bg='white',
    #                           fg='#001455',
    #                           justify=tkinter.RIGHT)
    #     label.place(x=self.w - l_width-20, y=self.h - 90, width = l_width, height=70)
    #
    # def talk_icon(self):
    #     logo_image = Image.open('data/judy_logo.png')
    #     logo_image = logo_image.resize((50, 50))
    #     tk_logo_image = ImageTk.PhotoImage(logo_image)
    #
    #     self.logo_label = tkinter.Label(self.root,
    #                                image=tk_logo_image,
    #                                bg='white')
    #     self.logo_label.image = tk_logo_image
    #     # self.logo_label.place(x=20, y=40, width=50, height=50)
    #
    #
    # def show_logo(self):
    #     print('Showing logo!')
    #     self.logo_label.place(x=20, y=40, width=50, height=50)
    #     self.root.update()
    #
    # def hide_logo(self):
    #     print('Talk icon disappear!')
    #     self.logo_label.destroy()
    #     self.root.update()





