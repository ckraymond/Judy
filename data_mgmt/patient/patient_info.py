import datetime
from judylog.judylog import judylog

from api.bubbleapi import bubbleAPI
from .patient_bg import patientBG
from .patient_friends import patientFriends
from .patient_faqs import patientFAQ

class patientInfo:

    def __init__(self, bubble_creds):
        judylog.debug('patientInfo.__init__ > Getting patient information.')
        self.bubble_creds = bubble_creds
        self.birthday = None
        self.fname = None
        self.mname = None
        self.lname = None
        self.nname = None
        self.location = {}
        self.gender = None
        self.friends = []
        self.bg = None
        self.faqs = []

    def __str__(self):
        return_string = 'Patient Bio\n------------------------------------------------------'
        return_string += f'\n{self.fname} {self.mname} {self.lname}, NN: {self.nname}, BD: {self.bday}, Loc: {self.location}, Gen: {self.gender}'
        return_string += str(self.bg)
        return_string += str(self.friends)
        return return_string

    def import_data(self):
        '''
        Calls the Bubble API to populate any patient information currently stored there. Then maps the data against the mapping dict.
        :return:
        '''

        bubble_api = bubbleAPI(self.bubble_creds)
        response = bubble_api.get_exch_conv('user')[0]
        judylog.debug(f'patientInfo.import_data > {response}')

        #TODO: Ensure the we are handling when information is not available
        self.id = self.check_available(response, '_id')                           # The patient ID in Bubble which can be useful later
        self.fname = self.check_available(response, 'first_name')
        self.mname = self.check_available(response, 'middle_name')
        self.lname = self.check_available(response, 'last_name')
        self.nname = self.check_available(response, 'nickname')
        self.location = self.check_available(response, 'home')
        self.gender = self.check_available(response, 'gender')
        self.caretaker = self.check_available(response, 'caretaker')
        self.watchers = self.check_available(response, 'watcher')

        if type(response['bday']) is str:
            self.birthday = datetime.datetime.strptime(response['bday'],
                                                       '%Y-%m-%dT%H:%M:%S.%fZ')
        elif type(response['bday']) is datetime.datetime:
            self.birthday = response['bday']
        else:
            self.birthday = None

        self.bg = patientBG(bubble_api.get_exch_conv('interest'))                       # In Bubble the background info is not split into its own section

        self.import_friends(bubble_api)

        self.import_faqs(bubble_api)

    def check_available(self, dict, key):
        if key in dict.keys():
            return dict[key]
        else:
            return None

    def import_friends(self, bubble_api):
        '''
        Pulls the associated list of friends from the Bubble API and then maps them onto the user.
        :return:
        '''

        # Get the list of friends from the Bubble API
        friends_list = bubble_api.get_exch_conv('friends')

        self.friends = patientFriends(friends_list)

    def import_faqs(self, bubble_api):
        '''
        Pulls the faqs and then populated into the patient user profile.
        :param bubble_api:
        :return:
        '''

        faq_list = bubble_api.get_exch_conv('faq')

        for faq in faq_list:
            new_faq = patientFAQ(faq['question'], faq['answer'])        # decided not to include things like watcher
            self.faqs.append(new_faq)