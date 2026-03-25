import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = "mongodb+srv://mohan07:s2kS9hWyhq5bZfcs@cluster0.9pykb.mongodb.net/"
    SECRET_KEY = os.getenv("SECRET_KEY", "secret123")
