import logging

LOG_NAME = './judy.log'

logging.basicConfig(filename = LOG_NAME,encoding='utf-8', filemode = 'w', format='%(asctime)s-%(levelname)s-%(message)s')
judylog = logging.getLogger()
judylog.setLevel(logging.DEBUG)
