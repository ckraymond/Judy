'''
Module contains chatHistory, chatExchange, and chatConversation. These classes are designed to hold all informaiton
associated with previous queries and responses on Judy.
'''

import datetime

from api.bubbleapi import bubbleAPI
from .chat_conversation import chatConversation
from .chat_exchange import chatExchange
from judylog.judylog import judylog

class chatHistory:

    def __init__(self):
        judylog.info('chatHistory.__init__ > Loading the chat history')

        # Create empty lists for the exchanges and conversations
        self.exchanges = []
        self.conversations = []

    def import_data(self):

        # Load all of the conversations first since we will need to check the exchanges against them
        self.load_all_conversations()

        # Then load all of the exchanges
        self.load_all_exchanges()

        # Clean the exchange data and make sure they have summaries
        self.clean_exchanges()

        # Next we check the mappings of conversations and exchanges
        self.check_mappings()

        # Cleans the conversations by checking for missing items
        self.clean_conversations()

        # Finally, we resave all of the information that has been tagged to be adjusted
        self.save_history()

        # Identify conversations that need to be deleted and delete them
        self.remove_orph_convos()
        # TODO: Create the conversation delete function

    def __str__(self):
        return_value = ''
        for item in self.conversations:
            return_value = return_value + '\n' + str(item)
        return return_value

    def load_all_conversations(self):
        '''
        Purpose is to get all conversations from Bubble API and clean and sort them then to check accuracy,
        and align to the exchanges to make a nested structure.
        :return:
        '''

        judylog.info('chatHistory.load_all_conversations > Starting to load all of the conversations.')
        # Reset the history to be empty (just in case we use outside of __init__)
        self.conversations = []

        # Open the Bubble API and get all the exchanges stored
        loadAPI = bubbleAPI()
        api_response = loadAPI.get_records('conversation')  # Returns dict
        judylog.info(f'chatHistory.load_all_conversations > {str(api_response)[0:50]}')

        # Go through the JSON to ensure there is a value for each item. Will use append_line as empty entry.
        for conversation in api_response:
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

        judylog.info(f'chatHistory.load_all_conversations > Total conversations loaded: {len(self.conversations)}')

    def load_all_exchanges(self):
        '''
        Loads all of the exchanges from Bubble and then ingests them into the self.exchanges list.
        :return:
        '''
        judylog.info('chatHistory.load_all_exchangess > Pulling list of exchanges from Bubble API.')

        # Open the Bubble API and get all the exchanges stored
        #TODO: Incorporate pagination to be able to pull more than 100 records.
        loadAPI = bubbleAPI()
        api_response = loadAPI.get_records('chatexchange')          # Returns dict

        judylog.info(f'chatHistory.load_all_exchanges > Loaded {len(api_response)} exchanges from Bubble.')

        # Go through the JSON to ensure there is a value for each item. Will use append_line as empty entry.
        for exchange in api_response:
            append_line = {
                'query': None,
                'response': None,
                'date': None,
                'summary': None,
                'conversation': None,           # Has to be different due to naming conventions between Bubble and local
                '_id': None
            }

            for item in append_line.keys():
                if item in exchange:
                    append_line[item] = exchange[item]

            if append_line['query'] is not None and append_line['response'] is not None and append_line['date'] is not None:
                if append_line['query'] != '' and append_line['response'] != '' and append_line['date'] != '':
                    new_exchange = chatExchange(append_line['date'], append_line['query'], append_line['response'],
                                                append_line['summary'], append_line['_id'], append_line['conversation'])
                    self.exchanges.append(new_exchange)

                    judylog.info(f'chatHistory.load_all_exchanges > Added ID {append_line['_id']} to exchanges: {str(append_line)[0:50]}')
                else:
                    judylog.warn(f'chatHistory.load_all_exchanges > Did not add conversation: {append_line['_id']}')
            else:
                judylog.warn(f'chatHistory.load_all_exchanges > Did not add conversation: {append_line['_id']}')
        judylog.info(f'chatHistory.load_all_exchanges > Total exchanges loaded: {len(self.exchanges)}')

    def clean_exchanges(self):
        '''
        With conversations and exchanges loaded we now clean all of the exchanges to make sure they have applicable
        information.
        :return:
        '''
        # Remove lines when there is no query, response, or date
        judylog.info('chatHistory.clean_exchanges > Cleaning the exchange data.')

        # Review the exchanges and add summaries
        for item in self.exchanges:
            item.check_summary()

        judylog.info(f'chatHistory.clean_exchanges > Total exchanges after cleaning: {len(self.exchanges)}')

    def check_mappings(self):
        '''
        Function to iterate through the exchanges and ensure that each exchange has an associated conversations ID.
        :return:
        '''

        judylog.info('chatHistory.check_mappings > In the check_mappings function')

        # Sort the exchanges by date/time
        self.exchanges.sort(key = lambda x : x.date)

        # print('Sorting through exchanges...')
        # for exch in self.exchanges:
        #     print(exch.date)

        judylog.info(f'Sorting through these exchanges: {len(self.exchanges)}')

        # Iterate through the exchanges and see if they have an associated conversation
        for num in range(len(self.exchanges)):
            if (self.exchanges[num].conv_id is None or self.exchanges[num].conv_id == '' or
                    self.exchanges[num].conv_id not in self.get_conv_ids()):
                if num > 0:
                    difftime = abs(self.exchanges[num].date - self.exchanges[num-1].date)
                    if difftime.total_seconds() > 120:
                        self.create_initial_conv(self.exchanges[num])
                    else:
                        self.exchanges[num].conv_id = self.exchanges[num-1].conv_id
                        self.exchanges[num]._ns = True
                else:       # Create a new conversation, populate with date and then assign the new ID to the exchange
                    self.create_initial_conv(self.exchanges[num])

        print('Total exchanges after checking mapping: ', len(self.exchanges))
        print('Total conversations after checking mapping: ', len(self.conversations))

    def clean_conversations(self):
        '''
        Go through the conversations and check to make sure that they have all necessary fields. If not, generate them
        and flag to be saved.
        :return:
        '''

        for conv in self.conversations:
            if conv.summary in ['', None] or conv.keywords in ['', None, []] or conv.sentiment in ['', None]:
                judylog.info(f'Conversation to be updated for (summary, keywords, sentiment): {conv.id}')
                exch_list = self.get_exchanges(conv.id)

                conv.clean_conv(exch_list)
        judylog.info('Checked conversations and identified those to be updated.')


    def save_history(self):
        '''
        Iterates through the conversations and exchanges and saves any that have been marked to be updated.
        Cannot create new ones.
        :return:
        '''
        for exch in self.exchanges:
            if exch._ns is True:
                exch.post_exch()
                exch._ns = False

        for conv in self.conversations:
            if conv._ns is True:
                conv.post_conv()
                conv._ns = False

        print('History saved onto Bubble.')

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
        new_conversation.id = new_conversation.post_conv()
        new_conversation._ns = True

        judylog.info(f'Creating initial conversation and mapping conv: {exchange.conv_id} to: {exchange.id}')

        exchange.conv_id = new_conversation.id
        self.conversations.append(new_conversation)
        exchange._ns = True

    def add_exchange(self, exch):
        '''
        Take in a chatExchange object, adds it to the exchanges list and then uploads to Bubble.
        :param exch:
        :return:
        '''
        self.exchanges.append(exch)

        # TODO: Need to check against conversations to see if there is one it should be added to and gt the conv_id.

        exch.id = exch.post_exch()
        exch._ns = False

    def check_for_conv(self, exch):
        '''
        Checks the exchange provided to see if it belongs with a specific conversation.
        :param exch:
        :return:
        '''
        for exist_exch in self.exchanges:
            difftime = abs(exch.date - exist_exch.date)
            if difftime.total_seconds() < 120:
                self.create_initial_conv(exch)
                return

        self.create_initial_conv(exch)
        return

    def rev_conversations(self):
        '''
        Review the conversations to determine if any of them are completed and can be closed out.
        :return:
        '''

        max_conv = {'index': 0,'value': datetime.datetime.min}

        # Skip this if there are no conversations
        if len(self.conversations) == 0: return                             # Skip this if there are no conversations

        # Now find the most recent conversation
        for index in range(len(self.conversations)):
            if self.conversations[index].date > max_conv['value']:
                max_conv['index'] = index
                max_conv['value'] = self.conversations[index].date

        max_exch = {'index': 0, 'value': datetime.datetime.min}                              # Track the most recent conversation
        exch_list = []

        # Now find the most recent exchange in that conversation if it doesn't have a summary
        if self.conversations[max_conv['index']].summary in [None, '']:
            for index in range(len(self.exchanges)):
                if self.exchanges[index].conv_id == self.conversations[max_conv['index']].id:
                    exch_list.append(self.exchanges[index])
                if self.exchanges[index].date > max_exch['value']:
                    max_exch['index'] = index
                    max_exch['value'] = self.exchanges[index].date

        difftime = abs(datetime.datetime.now() - self.exchanges[max_exch['index']].date)
        if difftime.total_seconds() > 120:
            judylog.info('Cleaning conversation: ', self.id)
            self.clean_conv(exch_list)

    def get_conv_ids(self):
        '''
        Simple helper function to get all of the conversation IDs
        :return:
        '''
        conv_ids = []
        for conv in self.conversations:
            conv_ids.append(conv.id)

        return conv_ids

    def remove_orph_convos(self):
        '''
        Go through the conversations on Bubble and remove any that are not being called by excahnged.
        :return:
        '''
        judylog.info('chatHistory.remove_orph_convos > Checking for orphaned conversaitons.')
        convo_list = self.get_conv_ids()

        for exch in self.exchanges:
            if exch.conv_id in convo_list:
                convo_list.remove(exch.conv_id)

        api_connection = bubbleAPI()
        for conv_id in convo_list:
            api_connection.remove_conv(conv_id)
            judylog.info('chatHistory.remove_orph_convos > Removed conversation ID: ', conv_id)