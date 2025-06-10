# Import local libraries & modules
from gradioUI import *
import terminalUI
#Run functions
if __name__ == "__main__":
    UI = get_gradio_UI()
    UI.launch(share=True)
    # If gradioUI doesn't work, uncomment the below to run the program in terminal
    # terminalUI.prompt()

