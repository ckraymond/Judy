'''
Main function for calling the Judy program.
'''

from judy_mvp import judyMVP
from judylog.judylog import judylog
import platform                                 # Used to get the OS information
from user_credentials import get_user_credentials

judylog.info('__main__ > Initializing the program.')

# Testing component to add in user credentials
email, password = get_user_credentials('Colin Raymond')

# Check what the operating system is
print('You are running Judy version 0.1. Your operating system is: ', platform.system())
is_mac = True if platform.system().lower() == 'darwin' else False

# Determine if we want dev mode
dev_input = input('Would you like to run in dev mode? Y/N')
dev_mode = True if dev_input.lower() == 'y' else False
if dev_mode is True:
    print('\nIn Dev Mode')

# If OS is mac then choose what we want to run
mac_choice = None                   # Set this to none so it exists
if is_mac is True or dev_mode is True:
    print('\n\nYou are running on Mac or in Dev mode. This does not support multithreading.')
    print('1. Photo Gallery\n2. Voice Input\n3. Maintenance Routine')
    mac_choice = input('Which would you like to do?')

main = judyMVP(is_mac, mac_choice, dev_mode, email, password)