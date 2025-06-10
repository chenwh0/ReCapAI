# External libraries
import os
import gradio

# Local libraries & modules
from output import *
import recapai
from transcribe import aai_transcribe

# In cmd, quick setup of API key by entering: setx KEY_NAME "my_key"
ASSEMBLYAI_KEY = os.getenv('ASSEMBLYAI_KEY')
def UI_recapai(audio_file="./upload_audio/EarningsCall.wav", output_types=["pdf", "docx", "txt"], file_name="recapai"):
    """Runs recapai program on gradio online & sharable interface! Can be seperated into 3 main steps: Transcribe audio, AI recap transcript, save completion (recap) to desired file type(s)
        Parmeter: 
        audio_file -- str, Specifies path to file (default= ./upload_audio/EarningsCall.wav) 
        output_types -- list, Specifies which type(s) of file recap should be saved as. Can save as multiple file types. (default = pdf, docx, AND txt)
        recap_file_path -- str, Specifies path ONLY of outputted recap file (default = ./output_recap/)
        recap_file_name -- str, Specifies name of outputted recap file (default = EarningsCallRecap)
    Output:
        outputs -- list[str], file addresses of saved files (for gradio to display on UI)
    """
    # Transcribe audio
    transcript = aai_transcribe(ASSEMBLYAI_KEY, audio_file.name)
    os.remove(audio_file.name) # Remove audio file after transcription
    # AI recap the transcript
    recap_info = recapai.recap(transcript)
    # Save completion (recap) to desired file type(s), add file names to outputs so gradio can recieve them
    outputs = []
    for output_type in output_types:
        if output_type == "pdf":
          outputs.append(save_as_pdf(recap_info, file_name=file_name))
        elif output_type == "docx":
          outputs.append(save_as_docx(recap_info, file_name=file_name))
        elif output_type == "txt":
          outputs.append(save_as_txt(recap_info, file_name=file_name))
    return outputs

def get_gradio_UI():
    """Setup gradio UI object so that user inputs can be passed to UI_recapai for running the main components of the program
        Output:
            UI -- (gradio UI object) passes it to main so that it can be .launch() on web browser 
    """
    UI = gradio.Interface(UI_recapai,
    inputs=[
            gradio.File(label="Audio File"),
            gradio.Dropdown(["pdf", "docx", "txt"], multiselect=True, label="Save As", info="Select format(s) to save recap as"),
            gradio.Textbox(label="File Name")
            ],
    outputs=gradio.File(file_count="multiple", file_types=[".txt", ".docx", ".pdf"]),
    examples=[["./upload_audio/EarningsCall.wav", ["pdf", "txt"], "EarningsCallRecap"]]
    )
    return UI
