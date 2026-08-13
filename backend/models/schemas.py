from pydantic import BaseModel
from typing import List

class Sentiment(BaseModel):
    sentiment_label: str    
    explanation: str

class RecapaiFormat(BaseModel):
    key_points: List[str]
    summary: str
    tasks: List[str]
    sentiment: Sentiment    