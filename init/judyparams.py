'''
These are the constants used to connect with a MongodDB. To be saved for now but not used.
'''

MONGODB  = {
    'database': 'mongodb://localhost:27017/',
    'client': 'mydatabase'
}

'''
This is the parameter information used to connect with the OpenAI interface.
'''
OPENAI_QUERY = {
    'model': 'gpt-3.5-turbo',
    'temp': 0,
    'sys_content': 'You are a personal assistant for someone who has dimentia.' +
                   'Youre job is to help remind them of things while at the same time to reassure them.' +
                   'You should not tell them anything you do not know to be true.'
}

'''
GUI Paramters dictate what the GUI looks like.
'''
GUI_PARAMS = {
    'theme': 'LightBlue2',  # List can be found through sg.theme_previewer() or .list() functions
    'x_size': 900,
    'y_size': 400,
    'title': 'Judy v0.01',
    'chat_fn': 'chat_history.dat',
    'chat_history': ''
}

