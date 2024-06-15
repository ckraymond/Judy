'''
Main function for calling the Judy program.
'''

# THE LEGACY STUFF I WAS WORKING ON
# from judy_gui import judyGUI            # The main GUI for the program
# judy_beta = judyGUI()
# judy_beta.window_read()

# THIS IS FOR THE NEW MVP OF THE DEVICE
# from judy_mvp import judyMVP
# GUI = judyMVP()

# THIS IS FOR THE VOICE ACTIVATION PORTTION
from judy_voice import judyVoice
voice = judyVoice()

# version = input('Which version do you want to run?\n(1) GUI Version - Desktop\n(2) Rasberry Pi Version')
#
# if version == '1':
#     main_window = judyGUI()                 # Instantiates the main window of the program
#     main_window.window_read()                # Now we wait for user input®
# else:
#     program = judyMVP()