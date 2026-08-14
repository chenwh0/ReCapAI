# Libraries for making HTTP request
import os
from dotenv import load_dotenv
import requests
from time import sleep

load_dotenv()
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

def upload_audio(upload_to_url: str, api_key: dict, filepath: str):
    """Upload local file to AssemblyAI API returns uploaded audio file's url (str)"""
    with open(filepath, "rb") as file_data:
        response = requests.post(upload_to_url, headers=api_key, data=file_data)
    # Get returned uploaded_url from json-converted response 
    response.raise_for_status()
    return response.json()["upload_url"]

def start_transcription(transcript_url: str, api_key: dict, payload: dict):
    """Get uploaded audio file's transcriber id return full transcribing url(str) as polling endpoint"""
    # Make POST request to AssemblyAI API endpoint w/ payload & headers                                                                                                                             
    response = requests.post(transcript_url, json=payload, headers=api_key)
    response.raise_for_status()
    transcript_id = response.json()["id"]
    # Use transcript_id to create polling_endpoint
    return f"{transcript_url}/{transcript_id}"

def poll_transcription(polling_endpoint: str, api_key: dict):
    """Poll full transcribing url every 3 sec to check status of transcript job returns audio's transcription(str) if successful"""
    
    while True:
        response = requests.get(polling_endpoint, headers=api_key)
        response.raise_for_status()
        transcript_json = response.json()
        if transcript_json["status"] == "completed":
            transcript_text = transcript_json["text"]
            if not transcript_text: 
                raise ValueError("No transcript generated.")
            return transcript_text
        elif transcript_json["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcript_json['error']}")
        else:
            sleep(3)
    

def transcribe_audio(filepath: str, assemblyai_key: str):
    """Transcribe audio file in filepath returns transcript text (str)
    Uses polling technique (as recommended) to check AssemblyAI's transcribing job status every 3 secs.
        
    Parameters:
    filepath -- str, Audio file path
    aai_key -- str, AssemblyAI API key

    Returns:
    transcript_text -- str, transcription of audio file

    """
    
    # Create API headers & endpoints
    if not filepath or not assemblyai_key: 
        raise ValueError("Audio file & AssemblyAI key required.")
    
    aai_api_key = { "authorization": assemblyai_key }
    base_url = "https://api.assemblyai.com/v2"
    upload_to_url = base_url + "/upload"
    transcript_url = base_url + "/transcript"

    upload_url = upload_audio(upload_to_url, aai_api_key, filepath)
    # Poll API every 3 sec to check status of transcript job
    poll_endpoint = start_transcription(transcript_url, aai_api_key, { "audio_url": upload_url })
    transcript_text = poll_transcription(poll_endpoint, aai_api_key)
    return transcript_text