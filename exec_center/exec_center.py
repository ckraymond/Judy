class execCenter:
    '''
    Class to handle and route any specific local user queries
    '''

    def __init__(self):
        self.action = None
        self.exchange = None

    def execute(self, action):
        '''
        Call to execute the specific action that is taken.
        :param action:
        :param exchange:
        :return:
        '''

        self.action = action

        if self.action == 'tell_time':
            return 'It\'s time for a new watch!'
        else:
            raise ValueError('The action is not found in the action table.')