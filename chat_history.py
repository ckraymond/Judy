import datetime

class chatHistory:

    def __init__(self):
        self.history = []

    def __str__(self):
        return_value = ''
        for item in self.history:
            return_value = return_value + '\n' + str(item)
        return return_value

    def append(self, query, response):

        # Creates a new exchange
        new_exchange = chatExchange(datetime.datetime.now(),
                                    query,
                                    response)
        # TODO: Create a process to pull out keywords from the exchange

        self.history.append(new_exchange)

        # TODO: Need to automagically save the chat history

        print(self)

class chatExchange:

    def __init__(self,
                 datetime = datetime.datetime.now(),
                 query = '',
                 response = '',
                 keywords = []):
        self.datetime = datetime
        self.query = query
        self.response = response
        self.keywords = keywords

    def __str__(self):
        return f'{self.datetime} | {self.query[0:20]} | {self.response[0:20]}'