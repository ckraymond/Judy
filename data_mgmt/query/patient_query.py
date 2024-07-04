import json
import string
class patientQuery:
    def __init__(self, exchange):
        self.exchange = exchange            # This is the initial exchange
        self.routing = {                    # Dict to contain routing information for the query
            'local': False,
            'action': None,
            'vars': {}
        }

        # Load and process the action table ahead of time
        self.load_action_table()

    def load_action_table(self):
        '''
        Loads JSON file with all mapped out functions and cleans the queries so that there is maximum chance of coverage
        :return:
        '''
        self.action_table = []
        temp_action_table = json.load(open('./data_mgmt/query/query_forms.json', 'r'))

        for item in temp_action_table:
            action = {}
            action['name'] = item['name']
            action['vars'] = item['vars']
            action['action'] = item['action']
            action['queries'] = []
            for query in item['queries']:
                new_query = query.translate(str.maketrans('', '', string.punctuation)).lower()
                action['queries'].append(new_query)
            self.action_table.append(action)

    def determine_action(self):

        for item in self.action_table:
            # Clean the query to remove punctuation and capitalization
            query_no_punc = self.exchange.query.translate(str.maketrans('', '', string.punctuation)).lower()

            if query_no_punc in item['queries']:
                self.routing['local'] = True
                self.routing['action'] = item['action']
                self.routing['vars'] = item['vars']
                break

if __name__ == '__main__':
    from data_mgmt.chat.chat_exchange import chatExchange

    test = patientQuery(chatExchange(None, query='What time is it?'))
    test.determine_action()
