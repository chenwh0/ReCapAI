from pydantic import BaseModel, Field
from typing import List

class Sentiment(BaseModel):
    sentiment_label: str    
    explanation: str

class RecapaiFormat(BaseModel):
    key_points: List[str]
    summary: str
    tasks: List[str]
    sentiment: Sentiment    

class RecapResult(BaseModel):
    recap: RecapaiFormat
    output_filepath: str

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str
    assemblyai_key: str

class UserLogin(BaseModel):
    username: str
    password: str