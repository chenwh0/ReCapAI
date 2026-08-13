import os
from ollama import chat
from models.schemas import RecapaiFormat

MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

def llm_analyze(transcript: str) -> RecapaiFormat:
    """Returns a dictionary of the summaries"""

    prompt = f"""You are an AI assistant specializing in analyzing conversations. 
    Analyze the following transcript and return the results for: 
    1. Key Points: {get_key_points_instructions()}
    2. Summary: {get_summarize_instructions()}
    3. Tasks: {get_extract_tasks_instructions()}
    4. Sentiment: {get_sentiment_analysis_instructions()}
    Transcript: "{transcript}"
    """

    completion = chat(model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                format=RecapaiFormat.model_json_schema()
    )
    return RecapaiFormat.model_validate_json(completion.message.content)
    
def get_sentiment_analysis_instructions():
    """Return instructions to analyze tone & emotion"""
    return """
    Analyze the sentiment of the transcript.
    Identify if sentiment is positvive, negative, or neutral, and briefly explain why."""

def get_summarize_instructions():
    """Return instructions to summarize into 1 abstract paragraph"""
    return """
    Summarize the transcript into one concise paragraph. 
    Retain the most important points and avoid unnecessary details."""

def get_key_points_instructions():
    """List key points"""
    return """
    List the main points (important ideas, finidngs, or topics) in the transcript.  
    Return as list of concise points."""

def get_extract_tasks_instructions():
    """List action items (assignments, tasks, actions, etc.)"""
    return """
    Identify any tasks, assignments, or actions that were mentioned or agreed upon.
    Return them as a list. If there are none, return an empty list."""
