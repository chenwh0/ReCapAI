# External libraries
import os

# Local libraries & modules
from output import *
import recapai
from transcribe import aai_transcribe

# In cmd, quick setup of API key by entering: setx KEY_NAME "my_key"
ASSEMBLYAI_KEY = os.getenv('ASSEMBLYAI_KEY')

def terminal_recapai(audio_file="./upload_audio/EarningsCall.wav", output_types=["pdf","docx","txt"], recap_file_path="./output_recap/", recap_file_name="EarningsCallRecap"):
    """Runs recapai program! Can be seperated into 3 main steps: transcribe audio, AI recap transcript, completion (recap) to desired file type(s)
        audio_file -- Specifies path to file (default= ./upload_audio/EarningsCall.wav) 
        output_types -- Specifies which type(s) of file recap should be saved as. Can save as multiple file types. (default = pdf, docx, AND txt)
        recap_file_path -- Specifies path ONLY of outputted recap file (default = ./output_recap/)
        recap_file_name -- Specifies name of outputted recap file (default = EarningsCallRecap)
    """
    # Transcribe Audio
    transcript = aai_transcribe(ASSEMBLYAI_KEY, audio_file)
    # AI recap transcript
    recap_info = recapai.recap(transcript)
    # Save recap to desired file type(s)
    for output_type in output_types:
        if output_type == "pdf":
          save_as_pdf(recap_info, recap_file_path, recap_file_name)
        elif output_type == "docx":
          save_as_docx(recap_info, recap_file_path, recap_file_name)
        elif output_type == "txt":
          save_as_txt(recap_info, recap_file_path, recap_file_name)
def prompt():
    """Prompts for necessary user inputs in the terminal before passing them to recapai function"""
    run_default = input("Run default demonstration? (y/n) ")
    if run_default == "y":
        print("Demo: Recaps the EarningsCall.wav in 'upload_audio' folder & saves the resulting EarningsCallRecap file in 'output_recap' folder.")
        terminal_recapai()
    else:
        desired_output_types = []
        audio_file = input("Path to audio file. Ex: './upload_audio/':")
        for output_type in ["pdf", "docx", "txt"]:
            desired_output = input("Save recap as a ." + output_type + "? (y/n) ")
            if desired_output == "y":
                desired_output_types.append(output_type)
        recap_file_path = input("Path to store recap file. Ex: './output_recap/': ")
        recap_file_name = input("Name of recap file: ")
        terminal_recapai(audio_file, desired_output_types, recap_file_path, recap_file_name)
