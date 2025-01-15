from dotenv import load_dotenv
import os
import datetime

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_ENABLED = False