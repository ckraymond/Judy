'''
Main function for calling the Judy program.
'''

PATIENT_ID_MAP = {
    'Colin': '1717521410502x636157005519156100',
    'Abraham': '1719179936708x386825897272624200',
    'Donald': '1719179857582x686599819866020900'
}
PATIENT_ID = PATIENT_ID_MAP['Abraham']      #Will use this to only pull information assiciated with a particular pateint

from judy_mvp import judyMVP
from judylog.judylog import judylog
import platform                                 # Used to get the OS information
from user_credentials import get_user_credentials

judylog.info('__main__ > Initializing the program.')

# Testing component to add in user credentials
email, password = get_user_credentials('Donald Trump')

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