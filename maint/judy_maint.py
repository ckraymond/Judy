class judyMaint():
    '''
    Intended to run in the background and continually checking to see if there are any updates to the program.

    Specific actions are:
    - Update the exchanges.
    - Update the conversations.
    - Check for any new photos
    - Update the user preferences
    '''

    def __init__(self):
        self.test = True