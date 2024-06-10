import logging
import datetime
import json

from data.user_test_data import test_user_info

class promptCreate:

    def __init__(self, raw_query, user, history):
        logging.info('Generating the GPT prompt.')
        self.user = user                            # Gets the user info from the test data
        self.raw_query = raw_query                  # This is the overall prompt with the user's info
        self.messages = []
        self.last_five = history[-5:]

        self.gen_user_query_sys_prompt()            # Trigger creation of the system prompt when called

        # TODO: Integrate with cloud to pull the information from there

        # self.chat history # Get last five chat history
        # self.long_term_history # Get the long term chat history

    def gen_user_query_sys_prompt(self):
        '''
        The main function that creates the overall background prompt to ChatGPT. The prompt includes all applicable
        backgorund information on the user.
        :return:
        '''
        logging.error('THIS IS WHERE YOU NEED TO WORK. YOU NEED TO CREATE A FUNCTION TO CRAFT THE QUERY GIVEN THE QUERY, USER INFO, AND HISTORY.')

        self.system_prompt = {
            'instructions': 'You are a personal assistant named Judy for someone with dementia. You should follow the following rules ' +
                      'when providing any responses:\n' +
                      '- All responses should be no more than two sentences in length.\n' +
                      '- You should not provide any answer oyu are not sure of.\n' +
                      '- When possible remind the user ' +
                      'of things they might have already asked or information that they might have forgotten that' +
                      'could be relevant.\n' +
                      '- You should refer to the user by their first name occasionally.\n',
            'info': 'The following JSON formatted field contains information about the user you are talking to:',
            'family': 'The following JSON formatted fields contain information about the users friends and family:',
            'background': ''
            # TODO: Need to include another field that contains FAQs and add into Bubble as well.
        }

        self.update_info()
        self.update_family()
        self.update_background()
        self.consolidate_prompt()

        self.build_message()

    def update_info(self):
        '''
        This function updates the info section of the prompts.
        :return:
        '''

        new_info = {
            'User\'s First Name': self.user.fname,
            'User\'s Middle Name': self.user.mname,
            'User\'s Last Name': self.user.lname,
            'User\'s Nickname': self.user.nname,
            'User\'s Gender': self.user.gender
        }

        # Need to treat date slightly differently
        if self.user.bday is datetime.datetime:
            new_info['User\'s Birthday'] = datetime.datetime.strptime(self.user.bday, '%B %d, %Y')

        self.system_prompt['info'] += '\n' + json.dumps(new_info)

    def update_family(self):
        '''This takes all of the friends and family and puts it into a single jason format.'''

        for fam in self.user.friends.data:
            fam_json = self.update_single_person(fam)
            self.system_prompt['family'] += fam_json

    def update_single_person(self, fam):
        '''Updates a single person and returns the value'''

        # USe a mapping table to ensure that we have the info there
        fam_mapping = {
            'relationship': 'Relationship to User',
            'fname': 'First Name',
            'lname': 'Last Name',
            'nname': 'Nickname',
            'location': 'Home',
            'interests': 'Interests and Hobbies',
            'deceased': 'Are They Deceased'
        }
        fam_info = {}

        for key in fam:
            if key in fam_mapping.keys():
                if key == 'bday':
                    if type(key) is datetime.datetime:
                        fam_info['Birthday'] = fam['bday'].strftime('%B %d, %Y')
                    if type(key) is str:
                        fam_info['Birthday'] = (datetime.datetime.strptime(fam['bday'], '%Y-%m-%dT%H:%M:%S.%fZ').
                                                strftime('%B %d, %Y'))
                elif key == 'deceased':
                    if fam['deceased'] is True:
                        fam_info['Are They Deceased'] = "Yes"
                    else:
                        fam_info['Are They Deceased'] = "No"
                else:
                    fam_info[fam_mapping[key]] = fam[key]

        return json.dumps(fam_info)

    def update_background(self):
        for interest in self.user.bg.data:
            if interest == 'schools':
                self.system_prompt['background'] += ('\nThe user is interested in the following schools and you ' +
                                                     'should integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])
            elif interest == 'sports':
                self.system_prompt['background'] += ('\nThe user is interested in the following sports and teams and ' +
                                                     'you should integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])
            elif interest == 'foods':
                self.system_prompt['background'] += ('\nThe user is interested in the following foods and you should' +
                                                     'integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])
            elif interest == 'places':
                self.system_prompt['background'] += ('\nThe user is interested in the following places and you should' +
                                                     'integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])
            elif interest == 'hobbies':
                self.system_prompt['background'] += ('\nThe user has the following hobbies and you should' +
                                                     'integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])

    def build_message(self):
        self.messages.append({"role": "system", "content": self.system_prompt_str})
        for item in self.last_five:
            self.messages.append({"role": "user", "content": item.query})
            self.messages.append({"role": "assistant", "content": item.response})
        self.messages.append({"role": "user", "content": self.raw_query})

    def consolidate_prompt(self):
        self.system_prompt_str = ''

        for item in self.system_prompt:
            self.system_prompt_str += item


    # def gen_faqs(self):
    #     faqs_prompt = ''
    #
    #     if len(self.user_info['faqs']) > 0:
    #         faqs_prompt = 'The following questions and answers are ones I often ask: '
    #         for qna in self.user_info['faqs']:
    #             faqs_prompt += f'\nQuestion: {qna['question']}. Answer: {qna['answer']}.'
    #
    #     print(faqs_prompt)
    #     return faqs_prompt

