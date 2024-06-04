import requests         # For the call
import os               # Needed for the BUBBLE_API_TOKEN
class bubbleAPI:
    def __init__(self):
        self.api_token = os.environ['BUBBLE_API_TOKEN']
        self.base_url = 'https://colinkraymond.bubbleapps.io/version-test/api/1.1/obj'

    def get_records(self, type):
        '''
        Requests to get record of a certain tupe from Bubble.
        :param type:
        :return:
        '''
        call_url = self.base_url + '/' + type
        head = {'Authorization': 'token {}'.format(self.api_token)}

        response = requests.get(call_url, headers=head)

        return response

    def post_exch_rcds(self, exchange):
        call_url = self.base_url + '/' + 'Chat Exchange'
        head = {'Authorization': 'token {}'.format(self.api_token)}
        body = {
            'Date': str(exchange.datetime),
            'Query': exchange.query,
            'Response': exchange.response,
            'Summary': exchange.summary
        }

        response = requests.post(call_url, headers=head, json=body)
        response_json = response.json()
        return response_json['id']