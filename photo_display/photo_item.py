import tkinter              # Careful as this can only be called once

class photoItem:

    def __init__(self, image = '', date = '', location = '', people = ''):
        self.image = image                      # URL for where image is on Bubble CDN
        self.date = date                        # Datetime in str format of the date taken
        self.location = location                # Where the photo taken
        self.people = people                    # People in the photo

    def __str__(self):
        return f'{self.image} | {self.date} | {self.location} | {self.people}'