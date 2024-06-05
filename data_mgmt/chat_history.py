import datetime
import logging
import json

from api.openaiapi import openai_api_summary, openai_conv_info
from api.bubbleapi import bubbleAPI

logger = logging.getLogger(__name__)
class chatHistory:

    def __init__(self):
        self.exchanges = []
        self.conversations = []

        self.load_all_conversations()
        self.load_all_exchanges()

        # As a final check we clean the data which makes sure all items are there and saves
        self.clean_exchanges()
        self.check_mappings()
        # self.clean_conversations()

    def __str__(self):
        return_value = ''
        for item in self.conversations:
            return_value = return_value + '\n' + str(item)
        return return_value

    def load_all_exchanges(self):
        '''
        Loads all of the exchanges from Bubble and then ingests them into the self.exchanges list.
        :return:
        '''
        logger.info('Pulling list of exchanges from Bubble API.')

        # Open the Bubble API and get all the exchanges stored
        loadAPI = bubbleAPI()
        api_response = loadAPI.get_records('chatexchange')          # Returns dict

        # Go through the JSON to ensure there is a value for each item. Will use append_line as empty entry.
        for exchange in api_response['response']['results']:
            append_line = {
                'query': None,
                'response': None,
                'date': None,
                'summary': None,
                'conv_id': None,
                '_id': None
            }

            for item in append_line.keys():
                if item in exchange:
                    append_line[item] = exchange[item]

            if append_line['query'] is not None and append_line['response'] is not None and append_line['date'] is not None:
                if append_line['query'] != '' and append_line['response'] != '' and append_line['date'] != '':
                    new_exchange = chatExchange(append_line['date'], append_line['query'], append_line['response'],
                                                append_line['summary'], append_line['_id'], append_line['conv_id'] )
                    self.exchanges.append(new_exchange)
                    logging.info('Added line to exchanges:', append_line)

    def load_all_conversations(self):
        '''
        Purpose is to get all conversations from Bubble API and clean and sort them then to check accuracy,
        and align to the exchanges to make a nested structure.
        :return:
        '''

        self.conversations = []  # Reset the history to be empty just in case
        logger.info('Pulling list of conversations from Bubble API.')

        # Open the Bubble API and get all the exchanges stored
        loadAPI = bubbleAPI()
        api_response = loadAPI.get_records('conversation')  # Returns dict

        # Go through the JSON to ensure there is a value for each item. Will use append_line as empty entry.
        for conversation in api_response['response']['results']:
            append_line = {
                'summary': None,
                'sentiment': None,
                'date': None,
                '_id': None,
                'keywords': []
            }

            # Map the
            for item in append_line.keys():
                if item in conversation:
                    append_line[item] = conversation[item]

            new_conversation = chatConversation(append_line['_id'], append_line['sentiment'],
                                                append_line['summary'], append_line['keywords'], append_line['date'])

            self.conversations.append(new_conversation)


    def clean_exchanges(self):
        # Remove lines when there is no query, response, or date
        logging.info('Cleaning the data.')

        # Review the exchanges and add summaries
        for item in self.exchanges:
            if item.summary is None or item.summary == '':
                response = openai_api_summary(item.query, item.response)
                item.summary = response['summary']

                logging.info('Adding summary to: ', item.id)

                # Update in Bubble
                api_call = bubbleAPI()
                api_call.update_exch_rcds(item)
                logging.info('Updated exchange id: ', item.id)

    def check_mappings(self):
        # First ensure that every

        logging.info('Checking alignement of conversations and exchanges')

        # Sort the exchanges by date/time
        self.exchanges.sort(key = lambda x : x.date)

        # Iterate through the exchanges and see if they have an associated conversation
        for num in range(len(self.exchanges)):
            if self.exchanges[num].conv_id is None:
                if num > 0:
                    difftime = self.exchanges[num].date - self.exchanges[num-1].date
                    if difftime.total_seconds() > 120:
                        self.create_initial_conv(self.exchanges[num])
                    else:
                        self.exchanges[num].conv_id = self.exchanges[num-1].conv_id
                        self.exchanges[num]._ns = True
                else:       # Create a new conversation, populate with date and then assign the new ID to the exchange
                    self.create_initial_conv(self.exchanges[num])

        # Now check the conversations to see if we need to add anything.
        for convs in self.conversations:
            if convs.summary is None or convs.keywords is None or convs.sentiment is None:
                exch_list = self.get_exchanges(convs.id)

                conv_info = openai_conv_info(exch_list)

                convs.summary = conv_info['summary']
                convs.keywords = conv_info['keywords']
                convs.sentiment = conv_info['sentiment']

                convs._ns = True

        # Finally go through and save the adjusted Conversations and the adjusted exchanges
        bubble_connect = bubbleAPI()

        for conv in self.conversations:
            if conv._ns is True:
                bubble_connect.update_conv_rcds(conv)
                conv._ns = False

        for exch in self.exchanges:
            if exch._ns is True:
                bubble_connect.update_exch_rcds(exch)
                exch._ns = False

# TODO: Need to create function to check conversations against exchanges and make sure there are not ones that
    #  have no associated exchanges
# TODO: Need to create function to remove empty exchanges from Bubble through API


    def get_exchanges(self, conv_id):
        exch_list = []

        for exchange in self.exchanges:
            if exchange.conv_id == conv_id:
                exch_list.append(exchange)

        return exch_list


    def create_initial_conv(self, exchange):
        '''
        Given an exchange, this creates a new conversation, sends the ID to the exchange and sets its own ID.
        Note that we generate the summary and sentiment in a later stage,
        :param exchange:
        :return:
        '''
        new_conversation = chatConversation(date=exchange.date)
        new_conversation.id = new_conversation.post_conversation()
        exchange.conv_id = new_conversation.id
        self.conversations.append(new_conversation)
        exchange._ns = True

class chatExchange:
    def __init__(self,
                 date = None,
                 query = None,
                 response = None,
                 summary = None,
                 id = None,
                 conv_id = None):
        self.query = query
        self.response = response
        self.summary = summary
        self.id = id
        self.conv_id = conv_id
        self._ns = False                            # Flag to determine if there are unsaved changes to an exchange
        if date is not None:
            if type(date) is datetime.datetime:
                self.date = date
            else:
                self.date = datetime.datetime.strptime(date,
                                                       '%Y-%m-%dT%H:%M:%S.%fZ')  # The date of the first exchange in the conversation
        else:
            self.date = None
    def __str__(self):
        return f'{self.id} | {self.date} | {self.summary[0:20]} | {self.query[0:20]} | {self.response[0:20]} | {self.conv_id}'

class chatConversation:
    '''
    This class is designed for conversations, which are a collection of exchanges. The definition of a conversation
    is any series of exchanges that occur without a two minute pause between them.
    '''
    def __init__(self,
                 id = None,
                 sentiment = None,
                 summary = None,
                 keywords = [],
                 date = None):

        self.id = id                                                     # The unique conversation id
        self.sentiment = sentiment                                       # The sentiment of the conversation
        self.summary = summary                                           # A simple summary of the conversation
        self.keywords = keywords                                         # The keywords associated with this conversation
        self._ns = False                                # Does the conversation need to be save to Bubble
        if date is not None:
            if type(date) is datetime.datetime:
                self.date = date
            else:
                self.date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')     # The date of the first exchange in the conversation
        else:
            self.date = None
        #TODO: Generate functions to pull keywords from user's profile and generate for exchange and for conversation.

    def __str__(self):
        return f'{self.id} | {self.date} | {self.summary} | Sent: {self.sentiment} | Kwds: {len(self.keywords)}'

    def post_conversation(self):
        # Generates a new conversation in Bubble

        apiConnection = bubbleAPI()
        body = {
            'sentiment': self.sentiment,
            'summary': self.summary,
            'keywords': self.keywords,
            'date': str(self.date)
        }
        response = apiConnection.post_record('conversation', body)
        return response['id']
