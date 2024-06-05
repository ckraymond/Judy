import PySimpleGUI as sg                    # Base function for the simple GUI
import pygame
from gtts import gTTS

from data_mgmt.chat_history import chatHistory       # Class that stores the chat exchance
from api.openaiapi import openai_api_call     # Class that handles querying the OpenAI API
from soundprocessing import soundProcessing
from init.judyparams import GUI_PARAMS


class judyGUI:
    # Class to support the GUI for judy.

    def __init__(self):
        # TODO: Adjust dimensions to pull screen size and do a percentage
        self.chat_history = chatHistory()           # Creates the chat history and loads from the history file
        self.create_history_string()

        # Enact options for the window
        sg.theme(GUI_PARAMS['theme'])

        # Set the variables for the input and output
        # self.input = sg.Input(key='input', expand_x=True, expand_y=True)
        self.output = sg.Multiline(GUI_PARAMS['chat_history'], key='output', size=(700, 15), expand_x=True, expand_y=True)

        self.layout = [[sg.Push(), self.output, sg.Push()],
                  [sg.Push(), sg.Button('Ask Question', bind_return_key=True), sg.Button('Quit'), sg.Push()]]

        self.window = sg.Window(GUI_PARAMS['title'],
                                self.layout,
                                size=(GUI_PARAMS['x_size'], GUI_PARAMS['y_size']),
                                resizable=True)

    def window_read(self):
        # Class to await user input on the window

        while True:
            self.event, self.values = self.window.read()

            if self.event in ('Quit', None, sg.WIN_CLOSED):
                break
            elif self.event == 'Ask Question':
                self.submit_question()

    def submit_question(self):
        query = self.ask_question()
        response = openai_api_call(query, self.chat_history.history)                   # Reaches out to the API and submits the question
        self.chat_history.append(query, response)           # Updates the chat history and saves (eventually)
        self.chat_history.assign_ids()                      # Sets the conversation IDs

        self.create_history_string()
        self.window['output'].update(self.params['chat_history'])

        self.read_response(response)

    def ask_question(self):
        self.ask_layout = [[sg.Push()],[sg.Image('Judy.jpeg'),[sg.Push()]]]
        self.ask_window = sg.Window('Ask Your Question',
                                    self.ask_layout,
                                    size=(100, 100),
                                    resizable=True)
        recording = soundProcessing()
        query = recording.get_query()
        return query

    def create_history_string(self):
        # Default welcome
        GUI_PARAMS['chat_history'] = ''
        item = len(self.chat_history.history)-1

        while item >= 0:
            new_exchange = '\nQuestion: ' + self.chat_history.history[item].query + '\n\n' + 'Response: ' + self.chat_history.history[item].response + '\n' + '-' * 20 + '\n'
            GUI_PARAMS['chat_history'] += new_exchange
            item -= 1

    def read_response(self, response):
        language = 'en'
        myobj = gTTS(text = response, lang = 'en', slow=False)
        myobj.save('./temp/response.mp3')

        # Initialize the mixer module
        pygame.mixer.init()

        # Load the mp3 file
        pygame.mixer.music.load('./temp/response.mp3')

        # Play the loaded mp3 file
        pygame.mixer.music.play()
