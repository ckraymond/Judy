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

    def assign_ids(self):
        for item_num in range(len(self.history)):
            if self.history[item_num].conv_id is None:
                if item_num == 0:
                    self.set_conv_id(self.history[item_num])
                    print('Setting a new conversation_id.')
                else:
                    diff_time = self.history[item_num].datetime - self.history[item_num-1].datetime

                    if diff_time.total_seconds() < 60*60*2:      # Threshold is two min
                        self.history[item_num].conv_id = self.history[item_num-1].conv_id
                        print('Conversations are close together')
                    else:
                        self.set_conv_id(self.history[item_num])
                        print('Setting a new conversation_id.')

        print(self)

    def set_conv_id(self, chat_exchange):
        new_id = chat_exchange.datetime.strftime('%d%m%Y%H%M%S')
        chat_exchange.conv_id = new_id

    def create_chat_summaries(self):
        logging.info('This is where I will have OpenAI generated chat summaries.')

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
        self.summary = ''
        self.vector = [],
        self.conv_id = None

    def __str__(self):
        return f'{self.datetime} | {self.conv_id} | {self.query[0:20]} | {self.response[0:20]}'

    def generate_keywords(self):
        #TODO: Need to extract keywords from the text using an API call to OpenAI

        self.keywords = openai_api_keywords(self.query + self.response)
        print(self.keywords)

