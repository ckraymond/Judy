import logging
from datetime import datetime

class photoItem:

    def __init__(self, image = '', date = '', location = '', people = '', id = ''):
        self.image = image                      # URL for where image is on Bubble CDN
        self.date = date                        # Datetime in str format of the date taken
        self.location = location                # Where the photo taken
        self.people = people                    # People in the photo
        self.id = id                            # The unique ID for the photo as assigned by Bubble

    def __str__(self):
        return f'{self.image} | {self.date} | {self.location} | {self.people}'

    def convert_date(self):
        '''
        Converts the base string date time combo into a date object.
        :return:
        '''

        # Exits out if the type is not already a string
        if type(self.date) is not str:
            logging.error('photoItem.convert_date > The photo date is not a string: ', self.id)
            return False

        dt_date = datetime.strptime(self.date, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.date = datetime.strftime(dt_date, '%A %B %-d, %Y')

