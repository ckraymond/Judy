from judylog.judylog import judylog
import datetime

class promptCreate:

    def __init__(self, raw_query, user, history):
        judylog.info('promptCreate.__init__ > Generating the GPT prompt.')
        self.user = user                            # This is the patient information
        self.raw_query = raw_query                  # This is the overall prompt with the user's info
        self.messages = []
        self.last_five = history[-5:]

        self.gen_user_query_sys_prompt()            # Trigger creation of the system prompt when called


    def gen_user_query_sys_prompt(self):
        '''
        The main function that creates the overall background prompt to ChatGPT. The prompt includes all applicable
        background information on the user.
        :return:
        '''
        judylog.info('promptCreate.gen_user_query_sys_prompt > Starting to generate the complete prompt to ChatGPT.')

        self.system_instructions = ('You are a personal assistant named Judy for someone with dementia. ' +
                                    'You should follow the following rules when providing any responses:\n' +
                                    '- All responses should be no more than two sentences in length.\n' +
                                    '- When possible remind the user ' +
                                    'of things they might have already asked or information that they might have forgotten that' +
                                    'could be relevant.\n' +
                                    '- Understand that the user is speaking to you and then a device is transcribing it into text. ' +
                                    'What you type back is being read to the user.\n' +
                                    '- You should refer to the user by their first name occasionally.\n')
        self.system_prompt = {
            'info': 'This is some information you should know about me, the user:',
            'family': 'This is information about my friends and family:',
            'background': ''
        }

        # Update the patients infor, family, and background
        self.update_info()
        self.update_family()
        self.update_background()

        # Add the FAQ section if there are in fact FAQs
        if len(self.user.faqs) > 0:
            self.system_prompt['faqs'] = ('This is a list of questions along with their answers that I may ask. ' +
                                          'If I ask one of these questions, or something similiar you should respond' +
                                          ' with the answers as I\'ve given them here.')
            self.update_faqs()
        self.consolidate_prompt()

        self.build_message()

    def update_info(self):
        '''
        This function updates the info section of the prompts.
        :return:
        '''
        self.system_prompt['info'] = ''
        self.system_prompt['info'] += f'My name is {self.user.fname} {self.user.mname} {self.user.lname}'
        if self.user.nname not in [None, '']:
            self.system_prompt['info'] += f', but people call me {self.user.nname}'
        self.system_prompt['info'] += '.'

        # Need to treat date slightly differently
        if self.user.birthday is datetime.datetime:
            birthday = datetime.datetime.strptime(self.user.birthday, '%B %d, %Y')
            self.system_prompt['info'] += f'My birthday is {birthday}'

        judylog.debug(f'promptCreate.update_info > {self.system_prompt}')

    def update_family(self):
        '''This takes all of the friends and family and puts it into a single JSON format.'''

        for fam in self.user.friends.data:
            fam_str = self.update_single_person(fam)
            self.system_prompt['family'] += fam_str

    def update_single_person(self, fam):
        '''Updates a single person and returns the value'''
        judylog.debug(f'promptCreate.update_single_person > {fam}')
        fam_str = ''

        fam_str += f'\n{fam['fname']} {fam['lname']} is my {fam['relationship']}.'

        for key in fam:
            if key == 'nname':
                fam_str += f'{fam['fname']} {fam['lname']} has the nickname {fam['nname']}. '
            if key == 'location':
                fam_str += f'{fam['fname']} {fam['lname']} lives in {fam['location']}. '
            if key == 'interests':
                fam_str += f'{fam['fname']} {fam['lname']} interests and hobbies include {fam['interests']}. '
            if key == 'deceased' and fam[key] is True:
                fam_str += f'Unfortunately, {fam['fname']} {fam['lname']} is deceased. '
            if key == 'bday':
                if type(fam['bday']) is datetime.datetime:
                    birthday = fam['bday'].strftime('%B %d, %Y')
                if type(fam['bday']) is str:
                    birthday = (datetime.datetime.strptime(fam['bday'], '%Y-%m-%dT%H:%M:%S.%fZ').
                                            strftime('%B %d, %Y'))
                fam_str += f'{fam['fname']} {fam['lname']} was born on {birthday}. '

        return fam_str

    def update_background(self):
        for interest in self.user.bg.data:
            if interest == 'schools':
                self.system_prompt['background'] += ('\nI am interested in the following schools and you ' +
                                                     'should integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])
            elif interest == 'sports':
                self.system_prompt['background'] += ('\nI am interested in the following sports and teams and ' +
                                                     'you should integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])
            elif interest == 'foods':
                self.system_prompt['background'] += ('\nI am interested in the following foods and you should' +
                                                     'integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])
            elif interest == 'places':
                self.system_prompt['background'] += ('\nI am interested in the following places and you should' +
                                                     'integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])
            elif interest == 'hobbies':
                self.system_prompt['background'] += ('\nI have the following hobbies and you should' +
                                                     'integrate them into your response as appropriate: ' +
                                                     self.user.bg.data[interest])

    def update_faqs(self):
        '''
        This function adds the actual questions and answers to the faq section.
        :return:
        '''

        for faq in self.user.faqs:
            new_faq = f'\nQuestion: {faq.question}.\nAnswer: {faq.answer}.'
            self.system_prompt['faqs'] += new_faq

    def build_message(self):
        self.messages.append({"role": "system", "content": self.system_instructions})
        self.messages.append({"role": "user", "content": self.system_prompt_str})
        for item in self.last_five:
            self.messages.append({"role": "user", "content": item.query})
            self.messages.append({"role": "assistant", "content": item.response})
        self.messages.append({"role": "user", "content": self.raw_query})

        judylog.debug(f'promptCreate.build_message > {self.messages}')

    def consolidate_prompt(self):
        self.system_prompt_str = ''

        for item in self.system_prompt.keys():
            self.system_prompt_str += self.system_prompt[item]

