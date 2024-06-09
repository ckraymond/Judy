import datetime
import logging

from api.bubbleapi import bubbleAPI
from patient_friends import patientFriends
from patient_bg import patientBG

class patientInfo():

    def __init__(self):
        self.fname = ''
        self.mname = ''
        self.lname = ''
        self.nname = ''
        self.location = ''
        self.gender = ''
        self.bday = None
        self.friends = []
        self.bg = None

    def __str__(self):
        return_string = 'Patient Bio\n------------------------------------------------------'
        return_string += f'\n{self.fname} {self.mname} {self.lname}, NN: {self.nname}, BD: {self.birthday}, Loc: {self.location['address']}, Gen: {self.gender}'
        return_string += str(self.bg)
        return_string += str(self.friends)
        return return_string

    def import_data(self):
        '''
        Calls the Bubble API to populate any patient information currently stored there. Then maps the data against the mapping dict.
        :return:
        '''

        bubble_api = bubbleAPI()
        response = bubble_api.get_records('patient')['response']['results'][0]

        #TODO: Ensure the we are handling when information is not available
        self.id = response['_id']                           # The patient ID in Bubble which can be useful later
        self.fname = response['First Name']
        self.mname = response['Middle Name']
        self.lname = response['Last Name']
        self.nname = response['Nick Name']
        self.location = response['Location']
        self.gender = response['Gender']
        self.birthday = datetime.datetime.strptime(response['Birthday'],
                                                       '%Y-%m-%dT%H:%M:%S.%fZ')

        self.bg = patientBG(response)                       # In Bubble the background info is not split into its own section

        self.import_friends(bubble_api)
        # TODO: Still need to assign friends information

    def import_friends(self, bubble_api):
        '''
        Pulls the associated list of friends from the Bubble API and then maps them onto the user.
        :return:
        '''

        # Get the list of friends from the Bubble API
        friends_list = bubble_api.get_records('friends')['response']['results']

        self.friends = patientFriends(friends_list)

test = patientInfo()
test.import_data()
print(test)