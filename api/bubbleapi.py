import requests         # For the call
import os               # Needed for the BUBBLE_API_TOKEN

from judylog.judylog import judylog

class bubbleAPI:
    def __init__(self, patient_id):
        self.api_token = os.environ['BUBBLE_API_TOKEN']
        self.base_url = 'https://colinkraymond.bubbleapps.io/version-test/api/1.1/obj'
        self.wf_url = 'https://colinkraymond.bubbleapps.io/version-test/api/1.1/wf'
        self.patient_id = patient_id

    def get_records(self, type):
        '''
        Requests to get record of a certain type from Bubble.
        :param type:
        :return:
        '''
        recds_remaining = 1                   # Set this to 1 to start
        cursor = 0
        limit = 100                              # This will remain the same through all the calls
        cons_response = []
        judylog.info(f'bubbleAPI.get_records > Getting, {type}, records from Bubble.')

        while recds_remaining > 0:
            call_url = f'{self.base_url}/{type}?cursor={cursor}&limit={limit}&patient={self.patient_id}'
            head = {'Authorization': 'token {}'.format(self.api_token)}

            response = requests.get(call_url, headers=head)

            judylog.info(f'bubbleAPI.get_records > response: {str(response)[0:100]}')

            recds_remaining = response.json()['response']['remaining']
            cons_response.extend(response.json()['response']['results'])

            if response.json()['response']['remaining'] > 0:
                cursor += limit

        judylog.info(f'bubbleAPI.get_records > {cons_response[0:5]}')
        judylog.info(f'bubbleAPI.get_records > Total {type} records pulled: {len(cons_response)}')
        return cons_response

    def post_record(self, type, body):
        '''
        Posts a record of type to Bubble
        :param type:
        :param body:
        :return:
        '''
        judylog.info(f'Posting {type} record to Bubble.')
        post_url = self.base_url + '/' + type
        head = {'Authorization': 'token {}'.format(self.api_token)}

        body['patient'] = self.patient_id

        response = requests.post(post_url, headers=head, json=body)
        return response.json()

    def update_exch_rcds(self, exchange):
        judylog.info(f'Updating exchange (ID: {exchange.id}) to Bubble.')
        call_url = self.wf_url + '/' + 'put_exchange'
        head = {'Authorization': 'token {}'.format(self.api_token)}
        body = {
            'date': str(exchange.date),
            'query': exchange.query,
            'response': exchange.response,
            'summary': exchange.summary,
            'id': exchange.id,
            'conv_id': exchange.conv_id,
            'patient': self.patient_id
        }

        response = requests.post(call_url, headers=head, json=body)

        if response.json()['status'] == 'success':
            return response.json()
        else:
            judylog.error(f'Unable to update exchange id in Bubble: {body['id']}')
            judylog.error(response.json())
            return False
    #TODO: Need to add in error handling for when something doesn't work

    def update_conv_rcds(self, conv):
        judylog.info(f'Updating conversation (ID: {conv.id}) to Bubble.')
        call_url = self.wf_url + '/' + 'put_conversation'
        head = {'Authorization': 'token {}'.format(self.api_token)}
        body = {
            'date': str(conv.date),
            'summary': conv.summary,
            'sentiment': conv.sentiment,
            'keywords': ','.join(conv.keywords),
            'id': conv.id,
            'patient': self.patient_id
        }

        response = requests.post(call_url, headers=head, json=body)

        if response.json()['status'] == 'success':
            return response.json()
        else:
            judylog.error(f'Unable to update id in Bubble: {body['id']}')
            judylog.error(response.json())
            return False

    def remove_recd(self, type, id):
        '''
        Takes a conversation ID, connects to the bubble API and then removes it from Bubble.
        :return:
        '''

        judylog.info(f'bubbleAPI.remove_recd > Removing record (ID: {id}) from Bubble with workflow {type}.')
        call_url = f'{self.wf_url}/{type}'
        head = {'Authorization': 'token {}'.format(self.api_token)}
        body = {
            'id': id
        }

        response = requests.post(call_url, headers=head, json=body)

        if response.json()['status'] == 'success':
            return response.json()
        else:
            judylog.error(f'bubbleAPI.remove_recd > Unable to update id in Bubble: {body['id']}')
            judylog.error(response.json())
            return False