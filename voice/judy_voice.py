'''
Main class that runs the voice prompts on Judy.
'''

import speech_recognition as sr
from judylog.judylog import judylog
from gtts import gTTS
import pygame
from mutagen.mp3 import MP3
import time
from data_mgmt.chat.chat_exchange import chatExchange
from api.openaiapi import openAIGPT

class judyVoice:

    def __init__(self, settings, bubble_creds, dev_mode = False):
        self.settings = settings
        # obtain audio from the microphone
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.listening = True               # Keyword to determine if we should exit
        self.dev_mode = dev_mode
        self.bubble_creds = bubble_creds

        # Adjust for the ambient noise
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

    def listen(self, chat_history, patient_info):
        '''
        Simple listener that just waits to hear if the keyword is spoken
        :return:
        '''
        judylog.info('judyVoice.listen > Starting to listen through microphone.')

        self.listening = True

        while self.listening is True:
            # DEV MODE OVERRIDE
            if self.dev_mode is True:
                self.req_resp(None, chat_history, patient_info)
            else:
                with self.m as source:
                    audio_data = self.r.listen(source)
                    try:
                        text = self.r.recognize_google(audio_data = audio_data, language = 'en-US')
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
            self.read_text('What question did you have?')
            self.req_undst = False
            while self.req_undst is False:

                audio_req = self.r.listen(source)

                try:
                    text_req = self.r.recognize_google(audio_data=audio_req, language='en-US')
                except:
                    self.read_text('Sorry, I didn\'t quite catch that. Can you please say it again?')
                    judylog.warn('judyVoice.req_resp > Unable to recognize user request.')
                else:
                    print('req_resp > ', text_req)
                    self.req_undst = True
                    self.submit_question(text_req, chat_history, patient_info)

        return True


    def read_text(self, text):
        '''
        Simple function to read the users response.
        :param response:
        :return:
        '''
        accent = self.get_accent(self.settings['accent'])
        myobj = gTTS(text = text, lang = 'en', slow=False, tld = accent)
        myobj.save('./temp/response.mp3')

        pygame.mixer.init()                                         # Initialize the mixer module
        pygame.mixer.music.load('./temp/response.mp3')              # Load the mp3 file
        pygame.mixer.music.play()

        time.sleep(MP3("./temp/response.mp3").info.length)          # Pause the program while talking

    def get_accent(self, accent):
        accent_map = {
            'australian': 'com.au',
            'english': 'co.uk',
            'american': 'us',
            'canadian': 'ca',
            'indian': 'co.in',
            'irish': 'ie',
            'south african': 'co.za',
            'nigerian': 'com.ng'
        }

        try:
            return accent_map[accent.lower()]
        except:
            judylog.error(f'judyVoice.get_accent > Unable to find accent ({accent}) in mapping.')
            return 'us'

    def submit_question(self, query, chat_history, patient_info):
        # Create new exchange object and populate with the query
        new_exchange = chatExchange(self.bubble_creds, _ns = True)
        new_exchange.query = query

        # Get response via OpenAI
        gpt_api = openAIGPT()
        gpt_api.user_query(new_exchange.query, patient_info, chat_history.exchanges)
        new_exchange.response = gpt_api.run_query()

        #TODO: Double check exactly what is sent to ChatGPT

        # Add the exchange onto the list of exchanges
        chat_history.exchanges.append(new_exchange)
        chat_history.check_for_conv(new_exchange)                              # Determine what conversaiton the exch should be part of

        # Check through the history to see if any conversations have completed and if so add a summary
        chat_history.rev_conversations()

        # save any changes to Bubble before proceeding
        chat_history.save_history()

        # Finally read the response to the user
        self.read_text(new_exchange.response)

    def quit_program(self):
        #TODO: Need to add support for multithreading in here using an event
        self.listening = False
        return True
