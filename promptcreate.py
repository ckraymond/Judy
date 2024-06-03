import logging
import datetime

from testdata.user_test_data import test_user_info

class promptCreate:

    def __init__(self):
        logging.info('Generating the GPT prompt.')
        self.user_info = test_user_info         # Gets the user info from the test data
        self.user_prompt = ''                   # This is the overall prompt with the user's info

        # TODO: Integrate with cloud to pull the information from there

        # self.chat history # Get last five chat history
        # self.long_term_history # Get the long term chat history

    def gen_prompt(self):
        '''
        The main function that creates the overall background prompt to ChatGPT. The prompt includes all applicable
        backgorund information on the user.
        :return:
        '''
        self.prompts = {
            'biography': self.gen_bio(),
            'people': self.gen_people(),
            'places': self.gen_places(),
            'events': '',
            'dates': '',
            'asks': '',
            'interests': ''
        }

        for prompts in self.prompts.values():
            self.user_prompt += prompts

        print(self.user_prompt)

    def gen_bio(self):
        bio_prompt = {
            'name': '',
            'nname': '',
            'bday': '',
            'home': ''
        }
        return_prompt = ''

        bio_prompt['name'] = f'My name is {self.user_info['biography']['names']['fname']} {self.user_info['biography']['names']['mname']} {self.user_info['biography']['names']['lname']}. '
        if self.user_info['biography']['names']['nname'] is not None:
            bio_prompt['nname'] = f'My nickname is {self.user_info['biography']['names']['nname']}. '
        bio_prompt['bday'] = f'My birthday is {self.user_info['biography']['bday']}. '
        bio_prompt['home'] = f'I live in {self.user_info['biography']['home']}. '

        for prompts in bio_prompt.values():
            return_prompt += prompts

        return return_prompt

    def gen_people(self):
        people_prompt = ''

        print('Generating people')
        print(self.user_info['people'])

        for person in self.user_info['people']:
            people_prompt += self.create_person(person)

        return people_prompt


    def create_person(self, person):
        logging.info('Generating personal info.')

        per_prompts = {
            'name': '',
            'location': '',
            'bday': '',
            'interests': '',
            'deceased': ''
        }

        per_prompts['name'] = f'I have a {person['relationship']} named {person['fname']} {person['lname']}. '
        if person['location'] is not None:
            per_prompts['location'] = f'They live in {person['location']}. '
        if person['bday'] is not None:
            per_prompts['bday'] = f'Their birthday is {person['bday']}. '
        if len(person['interests']) > 0:
            per_prompts['interests'] = f'Their interests are {person['interests']}. '
        if person['deceased'] is True:
            per_prompts['deceased'] = 'They are deceased. '

        person_prompt = ''
        for prompt in per_prompts.values():
            person_prompt += prompt

        return person_prompt

test = promptCreate()
print(test.gen_prompt())
            
        
        
'''
def create_person(fname, lname, nname, relationship, location, bday, interests, deceased):
    return {
        'fname': fname,
        'lname': lname,
        'relationship': relationship,
        'location': location,
        'bday': bday,
        'interests': interests,
        'deceased': deceased
    }
'''