import requests         # For the call
import os               # Needed for the BUBBLE_API_TOKEN
import logging

class bubbleAPI:
    def __init__(self):
        self.api_token = os.environ['BUBBLE_API_TOKEN']
        self.base_url = 'https://colinkraymond.bubbleapps.io/version-test/api/1.1/obj'
        self.wf_url = 'https://colinkraymond.bubbleapps.io/version-test/api/1.1/wf'

    def get_records(self, type):
        '''
        Requests to get record of a certain tupe from Bubble.
        :param type:
        :return:
        '''
        logging.info('Getting ', type, 'records from Bubble.')
        call_url = self.base_url + '/' + type
        head = {'Authorization': 'token {}'.format(self.api_token)}

        response = requests.get(call_url, headers=head)
        return response.json()

    def post_record(self, type, body):
        '''
        Posts a record of type to Bubble
        :param type:
        :param body:
        :return:
        '''
        logging.info('Posting ', type, 'record to Bubble.')
        post_url = self.base_url + '/' + type
        head = {'Authorization': 'token {}'.format(self.api_token)}

        response = requests.post(post_url, headers=head, json=body)
        return response.json()

    def update_exch_rcds(self, exchange):
        logging.info('Updating exchange (ID: ', exchange.id, ') to Bubble.')
        call_url = self.wf_url + '/' + 'put_exchange'
        head = {'Authorization': 'token {}'.format(self.api_token)}
        body = {
            'date': str(exchange.date),
            'query': exchange.query,
            'response': exchange.response,
            'summary': exchange.summary,
            'id': exchange.id,
            'conv_id': exchange.conv_id
        }

        response = requests.post(call_url, headers=head, json=body)

        if response.json()['status'] == 'success':
            return response.json()
        else:
            logging.error('Unable to update exchange id in Bubble: ' + body['id'])
            logging.error(response.json())
            return False
    #TODO: Need to add in error handling for when something doesn't work

    def update_conv_rcds(self, conv):
        logging.info('Updating conversation (ID: ', conv.id, ') to Bubble.')
        call_url = self.wf_url + '/' + 'put_conversation'
        head = {'Authorization': 'token {}'.format(self.api_token)}
        body = {
            'date': str(conv.date),
            'summary': conv.summary,
            'sentiment': conv.sentiment,
            'keywords': ','.join(conv.keywords),
            'id': conv.id
        }

        response = requests.post(call_url, headers=head, json=body)

        if response.json()['status'] == 'success':
            return response.json()
        else:
            logging.error('Unable to update id in Bubble: ' + body['id'])
            logging.error(response.json())
            return False

    def remove_conv(self, id):
        '''
        Takes a conversation ID, connects to the bubble API and then removes it from Bubble.
        :return:
        '''

        logging.info('Removing conversation (ID: ', id, ') from Bubble.')
        call_url = self.wf_url + '/' + 'del_conversation'
        head = {'Authorization': 'token {}'.format(self.api_token)}
        body = {
            'id': id
        }

        response = requests.post(call_url, headers=head, json=body)

        print(response)

        if response.json()['status'] == 'success':
            return response.json()
        else:
            logging.error('Unable to update id in Bubble: ' + body['id'])
            logging.error(response.json())
            return False

