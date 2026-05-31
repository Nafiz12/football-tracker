import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    DATABASE   = os.environ.get('DATABASE', 'football.db')
    DEBUG      = os.environ.get('DEBUG', 'False') == 'True'