# Libraries for making HTTP request
import requests
import json
from time import sleep

def aai_transcribe(aai_key: str, file_address: str):
    """Transcribe audio file in file_address returns transcript text (str)
    Uses polling technique (as recommended) to check AssemblyAI's transcribing job status every 3 secs.
        
    Parameters:
    file_address -- str, Audio file path
    aai_key -- str, AssemblyAI API key

    Returns:
    transcript_text -- str, transcription of audio file

    """
    
    # Create API headers & endpoints
    base_url = "https://api.assemblyai.com/v2"
    upload_to_url = base_url + "/upload"
    transcript_url = base_url + "/transcript"
    aai_api_key = {
        "authorization": aai_key
    }

    # Upload local audio file
    upload_url = upload_file(upload_to_url, aai_api_key, file_address)
    
    # Create JSON payload with audio_url parameter
    payload = {
        "audio_url": upload_url
    }

    # Poll API every 3 sec to check status of transcript job
    poll_endpoint = get_poll_endpoint(transcript_url, aai_api_key, payload)
    transcript_text = poll_routinely(aai_api_key, poll_endpoint)
    
    return transcript_text

def upload_file(upload_to_url: str, api_key: str, file_address: str):
    """Upload local file to AssemblyAI API returns uploaded audio file's url (str)"""
    with open(file_address, "rb") as file:
        response = requests.post(upload_to_url,
                                headers=api_key,
                                data=file)
    # Get returned uploaded_url from json-converted response 
    upload_url = response.json()["upload_url"]
    return upload_url

def get_poll_endpoint(transcript_url: str, api_key: str, payload: str):
    """Get uploaded audio file's transcriber id return full transcribing url(str) as polling endpoint"""
    # Make POST request to AssemblyAI API endpoint w/ payload & headers                                                                                                                             
    response = requests.post(transcript_url, json=payload, headers=api_key)
    # Get json-converted response's ID. 
    transcript_id = response.json()['id']
    # Use transcript_id to create polling_endpoint
    polling_endpoint = f"{transcript_url}/{transcript_id}"
    return polling_endpoint

def poll_routinely(api_key: str, polling_endpoint: str):
    """Poll full transcribing url every 3 sec to check status of transcript job returns audio's transcription(str) if successful"""
    while True:
        transcript_json = requests.get(polling_endpoint, headers=api_key).json()
        # When status == completed, print text & break
        if transcript_json['status'] == 'completed':
            return transcript_json['text']
            break
        # When status == error, print error info
        elif transcript_json['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcript_json['error']}")
        else:
            sleep(3)



