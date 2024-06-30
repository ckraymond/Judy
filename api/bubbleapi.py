import requests         # For the call
import os               # Needed for the BUBBLE_API_TOKEN

from judylog.judylog import judylog

class bubbleAPI:
    def __init__(self, credentials):
        self.base_url = 'https://colinkraymond.bubbleapps.io/version-test/api/1.1/obj'
        self.wf_url = 'https://colinkraymond.bubbleapps.io/version-test/api/1.1/wf'
        self.credentials = credentials

    def get_token(self):
        '''
        Uses the users login and password to get a token for API calls.
        :return:
        '''
        call_url = f'{self.wf_url}/gen_api_token?email={self.credentials['email']}&pw={self.credentials['password']}'

        response = requests.get(call_url).json()
        judylog.info(f'bubbleAPI.get_token > Getting new API key using credentials for {self.credentials['email']}')

        self.credentials['api_token'] = response['response']['token']
        self.credentials['patient_id'] = response['response']['user_id']

    def check_response(self, response):
        '''
        Checks the JSON formed response and validates that the response was successfull. If not, returns the status.
        :param response:
        :return:
        '''

        if 'error_class' in response.keys():
            if response['error_class'] == 'Unauthorized' and response['translation'] == 'Invalid or expired token: None':
                return 'invalid_token'
        elif 'statusCode' in response.keys():
            if response['statusCode'] == 404:
                return 'data_type_not_found'
        else:
            return 'success'

    def get_exch_conv(self, type):
        '''
                Requests to get record of a certain type from Bubble.
                :param type:
                :return:
                '''
        recds_remaining = 1  # Set this to 1 to start
        cursor = 0
        limit = 100  # This will remain the same through all the calls
        response_list = []
        judylog.info(f'bubbleAPI.get_exch_conv > Getting, {type}, records from Bubble.')

        # Type should be in chatexchange or conversation
        allowed_types = ['conversation', 'chatexchange', 'user', 'friends', 'interest', 'photo', 'faq', 'message']
        if type not in allowed_types:
            raise ValueError(f'bubbleAPI.get_exch_conv > Type should be one of: {', '.join(allowed_types)}.')

        while recds_remaining > 0:
            call_url = f'{self.base_url}/{type}?cursor={cursor}&limit={limit}'
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.get(call_url, headers=head).json()

            # If call unsuccessful get a new token and try again
            if self.check_response(response) == 'invalid_token':
                # Try and get the token and then make the call again
                self.get_token()
                head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
                response = requests.get(call_url, headers=head).json()

            # Add the records into the response list and move the cursor to paganate
            response_list.extend(response['response']['results'])
            recds_remaining = response['response']['remaining']
            cursor += limit

        judylog.info(f'bubbleAPI.get_records > {response_list[0:5]}')
        judylog.info(f'bubbleAPI.get_records > Total {type} records pulled: {len(response_list)}')
        return response_list

    def get_settings(self):
        '''
        Used to get the patient's settings from Bubble.
        :return:
        '''

        judylog.info(f'bubbleAPI.get_settings > Getting patient and device settings from Bubble.')

        call_url = f'{self.base_url}/setting?'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        response = requests.get(call_url, headers=head).json()
        judylog.info(f'bubbleAPI.get_settings > response: {str(response)[0:100]}')

        # If call unsuccessful get a new token and try again
        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.get(call_url, headers=head).json()

        judylog.info(f'bubbleAPI.get_settings > {str(response)}')
        return response['response']['results'][0]

    def update_conv_rcds(self, conv):
        '''
        Updates a conversation record in Judy.
        :param conv:
        :return:
        '''
        judylog.info(f'bubbleAPI.update_conv_rcds > Updating conversation (ID: {conv.id}) to Bubble.')
        call_url = self.wf_url + '/' + 'put_conversation'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        body = {
            'date': str(conv.date),
            'summary': conv.summary,
            'sentiment': conv.sentiment,
            'keywords': ','.join(conv.keywords),
            'id': conv.id
        }

        response = requests.post(call_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.get(call_url, headers=head, json=body).json()

        if response['status'] == 'success':
            return response
        else:
            judylog.error(f'bubbleAPI.update_conv_rcds > Unable to update id in Bubble: {body['id']}')
            judylog.error(f'bubbleAPI.update_conv_rcds > {response}')
            return False

    def post_record(self, type, body):
        '''
        Posts a record of type to Bubble
        :param type:
        :param body:
        :return:
        '''
        print(f'bubbleAPI.post_record > Posting {type} record to Bubble.')
        post_url = self.base_url + '/' + type
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}

        body['patient'] = self.credentials['patient_id']
        body['caretaker'] = self.credentials['caretaker_id']
        body['watcher'] = self.credentials['watcher_ids']

        response = requests.post(post_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.post(post_url, headers=head, json=body).json()

        print(f'bubbleAPI.post_record > Response: {response}')
        return response

    def update_exch_rcds(self, exchange):
        judylog.info(f'bubbleAPI.update_exch_rcds > Updating exchange (ID: {exchange.id}) to Bubble.')
        call_url = self.wf_url + '/' + 'put_exchange'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        body = {
            'date': str(exchange.date),
            'query': exchange.query,
            'response': exchange.response,
            'summary': exchange.summary,
            'id': exchange.id,
            'conv_id': exchange.conv_id,
            'patient': self.credentials['patient_id'],
            'caretaker': self.credentials['caretaker_id'],
            'watcher': self.credentials['watcher_ids']
        }

        response = requests.post(call_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.post(call_url, headers=head, json=body).json()

        if response['status'] == 'success':
            return response
        else:
            judylog.error(f'Unable to update exchange id in Bubble: {body['id']}')
            judylog.error(response)
            return False
    #TODO: Need to add in error handling for when something doesn't work

    def remove_recd(self, type, id):
        '''
        Takes an ID, connects to the bubble API and then removes it from Bubble.
        :return:
        '''

        judylog.info(f'bubbleAPI.remove_recd > Removing record (ID: {id}) from Bubble with workflow {type}.')
        call_url = f'{self.wf_url}/{type}'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        body = {
            'id': id
        }

        response = requests.post(call_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.post(call_url, headers=head, json=body).json()

        if response['status'] == 'success':
            return response
        else:
            judylog.error(f'bubbleAPI.remove_recd > Unable to remove id in Bubble: {body['id']}')
            judylog.error(response)
            return False


if __name__ == '__main__':
    # Get the user credentials that we will use to log in to various things
    from user_credentials import get_user_credentials
    email, password = get_user_credentials('Donald Trump')
    credentials = {
        'email': email,
        'password': password,
        'patient_id': None,
        'api_token': None
    }

    print(credentials)
    test = bubbleAPI(credentials)
    users = test.get_exch_conv('interest')
    for user in users:
        print(user)
    print(credentials)