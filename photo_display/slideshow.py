import tkinter as tk
from PIL import Image, ImageTk
import time
import logging
import threading
import requests
from io import BytesIO
import screeninfo

# Import other classes from Judy photo slideshow
from .photocanvas import photoCanvas
from .imagebackground import imageBackground
from .photo_mgmt import photoMgmt
from .imagelabel import imageLabel

class slideShow:

    def __init__(self):
        # Gets the lists of photo data from Bubble
        self.photo_data = photoMgmt()
        self.get_monitor_info()
        self.delay = 2                              #The delay in seconds between each picture

        self.root = tk.Tk()
        self.root.title('Judy v0.1')
        self.root.geometry("%dx%d+0+0" % (self.screen_dims['x'], self.screen_dims['y']))
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")

        self.slideshow_start()
        # t_mic_controls = threading.Thread(target=self.mic_controls())

        # t_slideshow.start()
        # t_mic_controls.start()

        # t_slideshow.join()
        # t_mic_controls.join()

        # # Bind the keys for now
        # self.root.bind('<KeyPress>', lambda event: self.show_mic_label(event))
        # self.root.bind('<KeyRelease>', lambda event: self.hide_mic_label(event))
        #
        self.root.mainloop()

    def get_monitor_info(self):
        self.screen_dims = {}
        monitors = screeninfo.get_monitors()
        for mon in monitors:
            if mon.is_primary is True:
                self.screen_dims['x'] = mon.width
                self.screen_dims['y'] = mon.height

    def mic_controls(self):
        self.root.bind('<KeyPress>', lambda event: self.show_mic_label(event))
        self.root.bind('<KeyRelease>', lambda event: self.hide_mic_label(event))

    def slideshow_start(self):
        self.photo_canvas = photoCanvas(self.root, self.screen_dims)

        # TODO: Reinput the infinite loop when ready
        while True:
            for photo_item in self.photo_data.photo_list:
                # Download the image from the web
                img_path = requests.get(photo_item.image)
                image = Image.open(BytesIO(img_path.content))

                self.set_background(image, photo_item, self.delay)

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

        self.image_background = imageBackground(image, self.photo_canvas.canvas, self.root, self.screen_dims)
        try:
            self.image_label
        except:
            logging.warn('Label does not exist.')
        else:
            self.image_label.destroy_self(self.photo_canvas.canvas)
        self.image_label = imageLabel(self.photo_canvas.canvas, self.root, self.screen_dims, photo_item)

        self.root.update()
        time.sleep(delay)







