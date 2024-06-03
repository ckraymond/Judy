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
            'events': self.gen_events(),
            'interests': self.gen_interests(),
            'faqs': self.gen_faqs()
        }

        for prompts in self.prompts.values():
            self.user_prompt += prompts

    def gen_bio(self):
        '''
        Takes the biographical information and consolidates it into a single string which will be added to the query.
        :return:
        '''
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
        '''
        Takes the list of people and then generates a single string that concatenates all of them using the
        create_person helper function.
        :return:
        '''
        people_prompt = ''

        for person in self.user_info['people']:
            people_prompt += self.create_person(person)

        return people_prompt


    def create_person(self, person):
        '''
        Takes the person info and creates a single string with that persons information.
        :param person:
        :return:
        '''
        logging.info('Generating personal info.')

        per_prompts = {
            'name': '',
            'location': '',
            'bday': '',
            'interests': '',
            'deceased': ''
        }

        per_prompts['name'] = f'I have a {person['relationship']} named {person['fname']} {person['lname']}; '
        if person['location'] is not None:
            per_prompts['location'] = f'They live in {person['location']}; '
        if person['bday'] is not None:
            per_prompts['bday'] = f'Their birthday is {person['bday']}; '
        if len(person['interests']) > 0:
            per_prompts['interests'] = f'Their interests are {person['interests']}; '
        if person['deceased'] is True:
            per_prompts['deceased'] = 'They are deceased. '

        person_prompt = ''
        for prompt in per_prompts.values():
            person_prompt += prompt

        return person_prompt

    def gen_places(self):
        '''
        Generates a single string which has all of the places that are important to the user and why.
        :return:
        '''
        places_prompt = ''
        for place in self.user_info['places']:
            places_prompt = f'{place['name']} is important to me because {place['reason']}. '

        return places_prompt

    def gen_events(self):
        events_prompt = ''

        if len(self.user_info['events']) > 0:
            events_prompt = 'The following events are important to me: '
            for event in self.user_info['events']:
                events_prompt += (f'{event['name']} on {event['date']} is important because {event['description']},')
            events_prompt = events_prompt[:-1] + '.'

        return events_prompt

    def gen_interests(self):
        ints_prompt = ''

        if len(self.user_info['interests']) > 0:
            ints_prompt = f'I am really interested in the following things: {self.user_info['interests']}'

        return ints_prompt

    def gen_faqs(self):
        faqs_prompt = ''

        if len(self.user_info['faqs']) > 0:
            faqs_prompt = 'The following questions and answers are ones I often ask: '
            for qna in self.user_info['faqs']:
                faqs_prompt += f'\nQuestion: {qna['question']}. Answer: {qna['answer']}.'

        print(faqs_prompt)
        return faqs_prompt


# test = promptCreate()
# test.gen_prompt()
# print(test.user_prompt)