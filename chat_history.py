import datetime
import pickle
import logging

from api_integration import openai_api_keywords

logger = logging.getLogger(__name__)
class chatHistory:

    def __init__(self):
        self.fn = 'chat_history.dat'
        self.load()

    def __str__(self):
        return_value = ''
        for item in self.history:
            return_value = return_value + '\n' + str(item)
        return return_value

    def append(self, query, response):

        # Creates a new exchange
        new_exchange = chatExchange(datetime.datetime.now(),
                                    query,
                                    response)
        # TODO: Create a process to pull out keywords from the exchange
        self.history.append(new_exchange)
        self.history[-1].generate_keywords()
        self.save()

        # TODO: Need to automagically save the chat history

    def save(self):
    # TODO: Eventually have this calling a cloud storage endpoint
        with open(self.fn, 'wb') as file:
            pickle.dump(self.history, file)

    def load(self):
    # TODO: Eventually have this calling a cloud storage endpoint
        try:
            self.history= []
            with open(self.fn, 'rb') as file:
                self.history = pickle.load(file)
            logger.info('Loaded chat history from: ' + self.fn)
        except:
            self.history = []               # Clears out the history and we start afresh!
            logging.error('Unable to load file.')


class chatExchange:

    def __init__(self,
                 datetime = datetime.datetime.now(),
                 query = '',
                 response = '',
                 keywords = []):
        self.datetime = datetime
        self.query = query
        self.response = response
        self.keywords = keywords

    def __str__(self):
        return f'{self.datetime} | {self.query[0:20]} | {self.response[0:20]}'

    def generate_keywords(self):
        #TODO: Need to extract keywords from the text using an API call to OpenAI

        self.keywords = openai_api_keywords(self.query + self.response)
        print(self.keywords)

