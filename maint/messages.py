from api.bubbleapi import bubbleAPI
from judylog.judylog import judylog
import datetime

class messageHandler:
    def __init__(self, patient_id):
        self.messages = []
        self.patient_id = patient_id

    def get_messages(self):
        '''
        Routine to check and see if there are messages waiting on Bubble
        :return:
        '''

        # Pull the raw list of messages from Bubble
        judylog.info(f'messageHandler.clean_messages > Checking for messages on Bubble')
        api_connection = bubbleAPI(self.patient_id)
        new_messages = api_connection.get_records('messages')

        #TODO: Convert any dates and times into datetimes
        for msg in new_messages:
            msg['Modified Date'] = datetime.datetime.strptime(msg['Modified Date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            msg['Created Date'] = datetime.datetime.strptime(msg['Created Date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            msg['Expiration Date'] = msg['Modified Date'] + datetime.timedelta(hours = msg['Expiration'])

            # Creates and array with each of the alert triggers
            msg['Alert Triggers'] = []
            trig_time = datetime.datetime.now()
            while trig_time < msg['Expiration Date']:
                msg['Alert Triggers'].append(trig_time)
                trig_time += datetime.timedelta(minutes = msg['Frequency'])

        if len(self.messages) == 0:
            self.messages = new_messages

        else:
            id_list = []
            for message in self.messages:
                id_list.append(message['_id'])

            for index in range(len(new_messages)):
                if new_messages[index]['_id'] not in id_list:
                    self.messages.append(new_messages[index])

    def clean_messages(self):
        '''
        Goes through the messages and determines if there are any that need to be deleted
        :return:
        '''

        judylog.info(f'messageHandler.clean_messages > Cleaning messages')

        for msg in range(len(self.messages)-1, -1, -1):
            if self.messages[msg]['Expiration Date'] < datetime.datetime.now():
                judylog.info(f'messageHandler.clean_messages > Deleting message: {msg}')
                del_msg = self.messages.pop(msg)

                api_connection = bubbleAPI()
                print(api_connection.remove_recd('del_message', del_msg['_id']))


    def alert_messages(self):
        '''
        Goes through the messages and alerts user if any of the frequency thresholds have been hit
        :return:
        '''

        judylog.info(f'messageHandler.clean_messages > Validating if any messages should be announced')
        for msg in self.messages:
            if len(msg['Alert Triggers']) > 0:
                msg['Alert Triggers'].sort()
                if(msg['Alert Triggers'][0]) <= datetime.datetime.now():
                    #TODO Create the speech part of this.
                    print(msg['Message'])
                    msg['Alert Triggers'].pop(0)

if __name__ == "__main__":
    test_instance = messageHandler()
    test_instance.get_messages()
    test_instance.clean_messages()
    for msg in test_instance.messages:
        print(msg)
    test_instance.alert_messages()