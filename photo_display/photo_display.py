'''
Judy Photo Viewer

This module is part of the Judy program. It is intended to be run as a seperate thread for the product and will display photos that are uploaded through Bubble onto the device.
'''
from .slideshow import slideShow
from PIL import Image
import requests
from io import BytesIO
from .photo_mgmt import photoMgmt
import time

# TODO: Integrate into a settings function with the app.
PHOTO_WAIT = 5

class photoDisplay:

    def __init__(self):
        self.photo_data = photoMgmt()
        self.slideshow = slideShow()

        while True:
            for photo_item in self.photo_data.photo_list:
                # Download the image from the web
                img_path = requests.get(photo_item.image)
                image = Image.open(BytesIO(img_path.content))

                self.slideshow.set_background(image, photo_item, PHOTO_WAIT)

        self.slideshow.root.mainloop()