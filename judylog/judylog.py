import logging

LOG_NAME = 'judy.log'

class judyLog:
    def __init__(self):
        logging.basicConfig(filename = LOG_NAME,encoding='utf-8', filemode = 'w', format='%(process)d-%(levelname)s-%(message)s')
