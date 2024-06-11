import datetime
import logging

from api.bubbleapi import bubbleAPI
from api.openaiapi import openAIGPT

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
        self._ns = False                                                 # Does the conversation need to be save to Bubble
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

    def post_conv(self):
        '''
        Updates a converation in Bubble. If there is an ID it will update the conversation but if none then it posts
        a new one.
        :return:
        '''

        apiConnection = bubbleAPI()

        if self.id is None or self.id == '':
            # Create a new record and populate with the conversation information
            body = {
                'sentiment': self.sentiment,
                'summary': str(self.summary),
                'keywords': ",".join(self.keywords),
                'date': str(self.date)
            }

            response = apiConnection.post_record('conversation', body)

            try:
                logging.info('New conversation created, ID: ', response['id'])
                return response['id']
            except:
                logging.error('chat_history.post_conv > Unable to return response to new conversation post: ',
                              response)
                return False

        else:
            # Update the record since we already have an ID
            response = apiConnection.update_conv_rcds(self)
            try:
                return response['response']['conversation']['_id']
            except:
                logging.error('Unable to send response from update conversation: ',
                              response)
                return False

    def clean_conv(self, exch_list):
        '''
        Given the list of associated exchanges, this returns a summary, keywords, and sentiment of the conversation
        :param exch_list:
        :return:
        '''
        api_integration = openAIGPT()
        conv_info = api_integration.get_conv_summary(exch_list)

        self.summary = conv_info['summary']

        # Keywords are trick as they sometimes comethrough as a list and sometimes as a string
        try:
            self.keywords = [x.strip() for x in conv_info['keywords'].split(',')]
        except:
            self.keywords = conv_info['keywords']

        self.sentiment = conv_info['sentiment']

        self._ns = True
        return True