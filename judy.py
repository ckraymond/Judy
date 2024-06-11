'''
Main function for calling the Judy program.
'''

from judy_gui import judyGUI            # The main GUI for the program
from judy_mvp import judyMVP

program = judyMVP()

# version = input('Which version do you want to run?\n(1) GUI Version - Desktop\n(2) Rasberry Pi Version')
#
# if version == '1':
#     main_window = judyGUI()                 # Instantiates the main window of the program
#     main_window.window_read()                # Now we wait for user input®
# else:
#     program = judyMVP()