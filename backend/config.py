import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret!")
    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
    DQLITE_PATH = os.getenv("DQLITE_PATH", "data/logs.db")
