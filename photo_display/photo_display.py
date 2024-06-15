'''
Judy Photo Viewer

This module is part of the Judy program. It is intended to be run as a seperate thread for the product and will display photos that are uploaded through Bubble onto the device.
'''
from PIL import Image
import requests
from io import BytesIO
from .photo_mgmt import photoMgmt
import time

# TODO: Integrate into a settings function with the app.
PHOTO_WAIT = 5

class photoDisplay:

    def __init__(self, tk_screen):
        self.photo_data = photoMgmt()

        while True:
            for photo_item in self.photo_data.photo_list:
                response = requests.get(photo_item.image)
                image = Image.open(BytesIO(response.content))

                tk_screen.show_image(image, photo_item, PHOTO_WAIT)

    # def talk_icon(self):



