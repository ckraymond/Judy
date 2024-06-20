'''
Main function for calling the Judy program.
'''

from judy_mvp import judyMVP
from judylog.judylog import judylog
import platform                                 # Used to get the OS information

judylog.info('__main__ > Initializing the program.')

# Check what the operating system is
print('You are running Judy version 0.1. Your operating system is: ', platform.system())
is_mac = True if platform.system().lower() == 'darwin' else False

# Determine if we want dev mode
dev_input = input('Would you like to run in dev mode? Y/N')
dev_mode = True if dev_input.lower() == 'y' else False
if dev_mode is True:
    print('In Dev Mode')

# If OS is mac then choose what we want to run
mac_choice = None                   # Set this to none so it exists
if is_mac is True:
    print('You are running on Mac. This does not support multithreading.')
    print('1. Photo Gallery\n2. Voice Input\n3. Maintenance Routine')
    mac_choice = input('Which would you like to do?')

main = judyMVP(dev_mode, is_mac, mac_choice)