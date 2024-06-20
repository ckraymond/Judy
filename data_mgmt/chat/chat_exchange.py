import datetime

from api.bubbleapi import bubbleAPI
from api.openaiapi import openAIGPT
from judylog.judylog import judylog

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
            self.date = datetime.datetime.now()
    def __str__(self):
        return f'{self.id} | {self.date} | {str(self.summary)[:20]} | {str(self.query)[0:20]} | {str(self.response)[0:20]} | {self.conv_id}'

    def check_summary(self):
        api_connection = openAIGPT()

        judylog.debug(f'chatHistory.check_summary > Checking summary on {self.id} - {self.summary[0:50]}')

        if self.summary == '' or self.summary is None:
            response = api_connection.gen_summary(self.query, self.response)
            self.summary = response['summary']

            judylog.info(f'chatHistory.check_summary > Adding summary to ID {self.id} fill out as it is empty: {response['summary']}')

            # Set tag for the exchange to be saved again in the future
            self._ns = True

    def post_exch(self):
        # Generates a new exchange in Bubble

        if self.id is None or self.id == '':
            # Create new record if there is not already one.
            apiConnection = bubbleAPI()
            body = {
                'query': self.query,
                'response': self.response,
                'summary': self.summary,
                'conversation': self.conv_id,
                'date': str(self.date)
            }
            response = apiConnection.post_record('chatexchange', body)

            try:
                judylog.info('chatExchange.post_exch > New exchange posted to Bubble, ID: ', response['id'])
                return response['id']
            except:
                judylog.error('chatExchange.post_exch > Unable to post new exchange: ', response)
        else:
            # Update existing one if there is already an ID there.
            apiConnection = bubbleAPI()
            response = apiConnection.update_exch_rcds(self)
            return response['response']['exchange']['_id']