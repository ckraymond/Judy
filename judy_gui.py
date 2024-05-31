import PySimpleGUI as sg                    # Base function for the simple GUI
import pickle                               # Used to save and retrieve the chat history

from chat_history import chatHistory       # Class that stores the chat exchance
from api_integration import openai_api_call     # Class that handles querying the OpenAI API

import time
class judyGUI:
    # Class to support the GUI for judy.

    def __init__(self):
        self.params = {
            'theme': 'LightBlue2', # List can be found through sg.theme_previewer() or .list() functions
            'x_size': 900,
            'y_size': 400,
            'title': 'Judy v0.01',
            'default_msg': 'Welcome to Judy. Please ask your question above.',
            'chat_fn': 'chat_history.dat'
        }
        # TODO: Adjsut dimenstions to pull screen size and do a percentage
        self.chat_history = chatHistory()

        self.load_history()      # Get the previous conversations that have occured

        # Enact options for the window
        sg.theme(self.params['theme'])
        # sg.set_options(font=('Arial', 14))

        # Set the variables for the input and output
        self.input = sg.Input(key='input', expand_x=True, expand_y=True)
        self.output = sg.Multiline(self.params['default_msg'], key='output', size=(700, 15))

        self.layout = [[sg.Push(), self.input, sg.Push()],
                  [sg.Push(), self.output, sg.Push()],
                  [sg.Push(), sg.Button('Submit', bind_return_key=True), sg.Button('Quit'), sg.Push()]]

        self.window = sg.Window(self.params['title'],
                                self.layout,
                                size=(self.params['x_size'], self.params['y_size']),
                                resizable=False)

    def window_read(self):
        # Class to await user input on the window

        while True:
            self.event, self.values = self.window.read()

            if self.event in ('Quit', None, sg.WIN_CLOSED):
                break
            elif self.event == 'Submit':
                self.submit_question(self.values['input'])

    def submit_question(self, query):
        response = openai_api_call(query)                   # Reaches out to the API and submits the question
        self.chat_history.append(query, response)           # Updates the chat history and saves (eventually)

        self.window['input'].update('')                     # Clears the input window
        self.add_new_exchange(query, response)

    def add_new_exchange(self, query, response):
        '''
        Adds a new exchange in the ouput box in a formatted manner
        :param query:
        :param response:
        :return: None
        '''
        new_exchange = '\nQuestion: ' + query + '\n\n' + 'Response: ' + response + '\n' + '-' * 20 + '\n'
        self.window['output'].update(self.window['output'].get() + new_exchange)        # Appends the new echange onto what is already there
    def load_history(self):
        # Function to pull the saved chat history from a data file

        try:
            with open(self.params['chat_fn'], 'wb') as file:
                self.chat_history = pickle.load(file)

        except:
            print('Unable to load file: ', self.params['chat_fn'])

    def save_history(self):
        # Function to pull the saved chat history from a data file

        try:
            with open(self.params['chat_fn'], 'wb') as file:
                pickle.dump(self.chat_history, file)

        except:
            print('Unable to save to  file: ', self.params['chat_fn'])
