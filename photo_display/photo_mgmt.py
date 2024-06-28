'''
Judy Photo Viewer > Photo Management

Module that controls the maintenance and display of photos on Judy. This is what pulls photos from Bubble.
'''

from api.bubbleapi import bubbleAPI
from photo_display.photo_item import photoItem

class photoMgmt:

    def __init__(self, credentials):
        self.photo_list = []
        self.bubble_creds = credentials
        self.load_photo_urls()

    def load_photo_urls(self):
        api_connect = bubbleAPI(self.bubble_creds)
        self.data = api_connect.get_exch_conv('photo')

        for photo in self.data:
            new_photo = photoItem()

            if 'image' in photo.keys():
                new_photo.image = 'https:' + photo['image']
            if 'people' in photo.keys():
                new_photo.people = photo['people']
            if 'location' in photo.keys():
                new_photo.location = photo['location']
            if 'date' in photo.keys():
                new_photo.date = photo['date']
                new_photo.convert_date()

            self.photo_list.append(new_photo)



