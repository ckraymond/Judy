'''
Main class that runs the voice prompts on Judy.
'''

import speech_recognition as sr
import logging
from gtts import gTTS
import pygame
from mutagen.mp3 import MP3
import time
from data_mgmt.chat.chat_exchange import chatExchange
from api.openaiapi import openAIGPT

class judyVoice:

    def __init__(self):
        # obtain audio from the microphone
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.KEYWORD = 'judy'

        # Adjust for the ambient noise
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

    def listen(self, chat_history, patient_info):
        '''
        Simple listener that just waits to hear if the keyword is spoken
        :return:
        '''
        logging.info('Starting to listen through microphone.')

        while True:
            with self.m as source:
                audio_data = self.r.listen(source)
                try:
                    text = self.r.recognize_google(audio_data = audio_data, language = 'en-US')
                except:
                    print('listen > Unable to distinguish audio.')
                else:
                    print('listen > ', text)

                    if self.KEYWORD in text.lower():
                        print('Keyword found in: ', text)
                        self.req_resp(source, chat_history, patient_info)

    def req_resp(self, source, chat_history, patient_info):
        self.read_text('What question did you have?')
        self.req_undst = False
        while self.req_undst is False:

            audio_req = self.r.listen(source)

            try:
                text_req = self.r.recognize_google(audio_data=audio_req, language='en-US')
            except:
                self.read_text('Sorry, I didn\'t quite catch that. Can you please say it again?')
                logging.warn('Unable to recognize user request.')
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
        myobj = gTTS(text = text, lang = 'en', slow=False, tld = 'co.uk')
        myobj.save('./temp/response.mp3')

        pygame.mixer.init()                                         # Initialize the mixer module
        pygame.mixer.music.load('./temp/response.mp3')              # Load the mp3 file
        pygame.mixer.music.play()

        time.sleep(MP3("./temp/response.mp3").info.length)          # Pause the program while talking

    def submit_question(self, query, chat_history, patient_info):
        # Create new exchange object and populate with the query
        new_exchange = chatExchange()
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
