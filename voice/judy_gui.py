import PySimpleGUI as sg                    # Base function for the simple GUI
import pygame
from gtts import gTTS
import judylog
import mutagen

from data_mgmt.chat.chat_history import chatHistory, chatExchange       # Class that stores the chat exchance
from api.openaiapi import openAIGPT     # Class that handles querying the OpenAI API
from soundprocessing import soundProcessing
from init.judyparams import GUI_PARAMS
from data_mgmt.patient.patient_info import patientInfo


class judyGUI:
    # Class to support the GUI for judy.

    def __init__(self):
        '''
        Initializes the relatively simple GUI and waits for user instruction.
        '''
        # TODO: Adjust dimensions to pull screen size and do a percentage
        self.chat_history = chatHistory()           # Creates the chat history and loads from the history file

        self.patient_info = patientInfo()           # Gets the patient's information
        self.patient_info.import_data()

        self.layout = [[sg.Push(), sg.Image('./data/judy_circle.png', subsample=5), sg.Push()],
                       [sg.Push(), sg.Button('Ask Question', bind_return_key=True), sg.Button('Quit'), sg.Push()]]

        self.window = sg.Window(GUI_PARAMS['title'],
                                self.layout,
                                size=(GUI_PARAMS['x_size'], GUI_PARAMS['y_size']),
                                resizable=True)

        judylog.info('Judy GUI Initialized.')

    def window_read(self):
        '''
        Function loops through until user clicks quit
        :return:
        '''

        while True:
            self.event, self.values = self.window.read()

            if self.event in ('Quit', None, sg.WIN_CLOSED):
                self.close_out()
                break
            elif self.event == 'Ask Question':
                self.submit_question()

    def submit_question(self):
        # Create new exchange object and populate with the ask_question function
        new_exchange = chatExchange()
        new_exchange.query = self.ask_question()
        # new_exchange.query = 'This is a test, can you hear me?'

        # Get response via OpenAI
        gpt_api = openAIGPT()
        gpt_api.user_query(new_exchange.query, self.patient_info, self.chat_history.exchanges)
        new_exchange.response = gpt_api.run_query()

        #TODO: Double check exactly what is sent to ChatGPT

        # Add the exchange onto the list of exchanges
        self.chat_history.exchanges.append(new_exchange)
        self.chat_history.check_for_conv(new_exchange)                              # Determine what conversaiton the exch should be part of

        # Check through the history to see if any conversations have completed and if so add a summary
        self.chat_history.rev_conversations()

        # save any changes to Bubble before proceeding
        self.chat_history.save_history()

        # Finally read the response to the user
        self.read_response(new_exchange.response)
        #TODO: Find a way to halt other operations until the response is complete

    def ask_question(self):
        self.ask_layout = [[sg.Push()],[sg.Image('Judy.jpeg'),[sg.Push()]]]
        self.ask_window = sg.Window('Ask Your Question',
                                    self.ask_layout,
                                    size=(100, 100),
                                    resizable=True)
        recording = soundProcessing()
        query = recording.get_query()
        return query

    def read_response(self, response):
        '''
        Simple function to read the users response.
        :param response:
        :return:
        '''
        myobj = gTTS(text = response, lang = 'en', slow=False)
        myobj.save('./temp/response.mp3')

        pygame.mixer.init()                                         # Initialize the mixer module
        pygame.mixer.music.load('../temp/response.mp3')              # Load the mp3 file
        pygame.mixer.music.play()                                   # Play the loaded mp3 file

    def close_out(self):
        '''
        This function is run when the app is closed out. It checks the data and then runs a save
        :return:
        '''

        # Clean the exchange data and make sure they have summaries
        self.chat_history.clean_exchanges()

        # Next we check the mappings of conversations and exchanges
        self.chat_history.check_mappings()

        # Cleans the conversations by checking for missing items
        self.chat_history.clean_conversations()

        # Finally, we resave all of the information that has been tagged to be adjusted
        self.chat_history.save_history()