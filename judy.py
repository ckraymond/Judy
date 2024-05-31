'''
Main function for calling the Judy program.
'''

from judy_gui import judyGUI            # The main GUI for the program

main_window = judyGUI()                 # Instantiates the main window of the program
main_window.window_read()                # Now we wait for user input

# RESERACH
# https://scalexi.medium.com/implementing-a-retrieval-augmented-generation-rag-system-with-openais-api-using-langchain-ab39b60b4d9f

# NOTES
# TODO: Add support for logging
# Review concept of RAG with the system
# Store chat history so it can be remembered in perpetuity
# Think about way to compress chat history
# Look more at the personal history file
# Create AWS function and folder to emulate cloud storage