'''
Judy Photo Viewer

This module is part of the Judy program. It is intended to be run as a seperate thread for the product and will display photos that are uploaded through Bubble onto the device.
'''

from .slideshow import slideShow
from .photo_mgmt import photoMgmt


# TODO: Integrate into a settings function with the app.
PHOTO_WAIT = 5

class photoDisplay:

    def __init__(self):
        self.photo_data = photoMgmt()
        self.slideshow = slideShow(self.photo_data, PHOTO_WAIT)