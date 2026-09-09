import os
os.environ["JWT_SECRET_KEY"] = "test-secret-key-that-is-at-least-32-bytes-long"
os.environ["JWT_ALGORITHM"] = "HS256"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


from backend.main import app
from backend.database.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool,
                       ) # StaticPool ensures tests use same in-memory database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally: 
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Test registration

# Successful registration
def test_registration_success():
    response = client.post("/register", 
                           json={
                               "username": "testuser",
                               "password": "testpassword",
                               "assemblyai_key": "fake_assemblyai_key"
                           })
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully."

# Duplicate registration
def test_registration_duplicate():
    user_data = {
        "username": "duplicateuser",
        "password": "testpassword",
        "assemblyai_key": "fake_assemblyai_key"
    }
    client.post("/register", json=user_data)

    # Try to register again with same credentials
    response = client.post("/register", json=user_data)
    
    assert response.status_code == 409
    assert response.json()["detail"] == "Username already exists."



# Test login

# Successful login
def test_login_success():
    user_data = {
        "username": "loginuser",
        "password": "testpassword",
        "assemblyai_key": "fake_assemblyai_key"
    }
    client.post("/register", json=user_data)
    response = client.post("/login", json={"username": user_data["username"], "password": user_data["password"]})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# Incorrect password login
def test_login_incorrect_password():
    user_data = {
        "username": "incorrectpassworduser",
        "password": "testpassword",
        "assemblyai_key": "fake_assemblyai_key"
    }
    client.post("/register", json=user_data)
    response = client.post("/login", json={"username": user_data["username"], "password": "wrongpassword"})

    assert response.status_code == 401