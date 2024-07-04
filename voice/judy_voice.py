'''
Main class that runs the voice prompts on Judy.
'''

import speech_recognition as sr
from judylog.judylog import judylog
from voice.sound_handler import soundHandler
from data_mgmt.query.patient_query import patientQuery
from data_mgmt.chat.chat_exchange import chatExchange
from api.openaiapi import openAIGPT
from exec_center.exec_center import execCenter
import random

class judyVoice:

    def __init__(self, settings, bubble_creds, dev_mode = False):
        self.settings = settings
        self.sound_handler = soundHandler(self.settings['accent'])

        self.listening = True               # Keyword to determine if we should exit
        self.dev_mode = dev_mode
        self.bubble_creds = bubble_creds

    def listen(self, chat_history, patient_info):
        '''
        Simple listener that just waits to hear if the keyword is spoken
        :return:
        '''
        judylog.info('judyVoice.listen > Starting to listen through microphone.')

        self.listening = True

        while self.listening is True:
            if self.dev_mode is True:
                self.req_resp(None, chat_history, patient_info)
            else:
                with self.sound_handler.m as source:
                    audio_data = self.sound_handler.r.listen(source)
                    print('judyVoice.listen > Continuing to wait for prompt')
                    try:
                        text = self.sound_handler.r.recognize_google(audio_data = audio_data, language = 'en-US')
                    except:
                        print('judyVoice.listen > Unable to distinguish audio.')
                    else:
                        print('judyVoice.listen > User dialog: ', text)

                        if self.settings['trigger'].lower() in text.lower():
                            print('Keyword found in: ', text)
                            self.req_resp(source, chat_history, patient_info)

                        if 'quit program' in text.lower():
                            print('Quitting program')
                            self.quit_program()

    def req_resp(self, source, chat_history, patient_info):
        # Dev Mode override so I can type questions
        if self.dev_mode is True:
            text_req = input('What is your question for Judy?')

            if 'quit program' in text_req.lower():
                print('Quitting program')
                self.quit_program()
            else:
                self.submit_question(text_req, chat_history, patient_info)

        else:
            self.sound_handler.read_text(self.rand_response())
            self.req_undst = False
            while self.req_undst is False:

                audio_req = self.sound_handler.r.listen(source)

                try:
                    text_req = self.sound_handler.r.recognize_google(audio_data=audio_req, language='en-US')
                except:
                    self.sound_handler.read_text('Sorry, I didn\'t quite catch that. Can you please say it again?')
                    judylog.warn('judyVoice.req_resp > Unable to recognize user request.')
                else:
                    print('req_resp > ', text_req)
                    self.req_undst = True
                    self.submit_question(text_req, chat_history, patient_info)

        return True

    def submit_question(self, query, chat_history, patient_info):
        # Create new exchange object and populate with the query
        new_exchange = chatExchange(self.bubble_creds, _ns = True)
        new_exchange.query = query

        # Now we need to check if there is local action to take or we send to ChatGPT
        query_action = patientQuery(new_exchange)
        query_action.determine_action()

        if query_action.routing['local'] is False:
            # Get response via OpenAI
            gpt_api = openAIGPT()
            gpt_api.user_query(new_exchange.query, patient_info, chat_history.exchanges)
            new_exchange.response = gpt_api.run_query()

        else:
            local_action = execCenter()
            new_exchange.response = local_action.execute(query_action.routing['action'])

        # Add the exchange onto the list of exchanges
        chat_history.exchanges.append(new_exchange)
        chat_history.check_for_conv(new_exchange)                              # Determine what conversaiton the exch should be part of

        # Check through the history to see if any conversations have completed and if so add a summary
        chat_history.rev_conversations()

        # save any changes to Bubble before proceeding
        chat_history.save_history()

        # Finally read the response to the user
        self.sound_handler.read_text(new_exchange.response)


    def quit_program(self):
        #TODO: Need to add support for multithreading in here using an event
        self.listening = False
        return True

    def rand_response(self):
        response_strings = [
            'How can I help you?',
            'What\'s going on?',
            'What do you need?',
            'Hope you are doing well. Anything I can do to assist?',
            'You rang?'
        ]

        index = random.randint(0,len(response_strings)-1)
        return response_strings[index]

