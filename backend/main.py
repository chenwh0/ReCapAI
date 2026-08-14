from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from pathlib import Path
from tempfile import NamedTemporaryFile
import shutil

from .database.database import Base, engine, get_db
from .database.models import User
from .auth.auth import hash_password, verify_password, create_access_token
from .auth.dependencies import get_current_user
from .pipeline import RecapPipeline
from .models.schemas import RecapResult, UserCreate, UserLogin

Base.metadata.create_all(bind=engine) # Create all database tables from Declarative Base class
app = FastAPI()

# For React frontend to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

pipeline = RecapPipeline()

# Routes 
@app.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Search by username matches, stop search if first match found
    existing_user = (db.query(User).filter(User.username == user_data.username).first())
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists.")
    user = User(username=user_data.username, password_hash=hash_password(user_data.password), assemblyai_key=user_data.assemblyai_key)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully."}

@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.username == user_data.username).first())
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username/password.")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/recap", response_model=RecapResult)
async def recap_audio(audio_file: UploadFile=File(...), current_user: User = Depends(get_current_user), model_name: str = Form(...), export_type: str = Form(...)):
    temp_path = None
    try: 
        with NamedTemporaryFile(delete=False, suffix=Path(audio_file.filename).suffix) as temp_file:
            shutil.copyfileobj(audio_file.file, temp_file)
            temp_path = temp_file.name
        return pipeline.recap(temp_path, current_user.assemblyai_key, model_name, export_type)
    except Exception as error_message:
        raise HTTPException(status_code=500, detail=str(error_message))
    finally: # Whether success/failed, always delete temp file
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)


@app.get("/health")
def health():
    return {"status": "running"}