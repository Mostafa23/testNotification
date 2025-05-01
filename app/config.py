# config.py

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

MONGODB_URI_LOCAL = os.getenv("MONGODB_URI_LOCAL")
MONGODB_URI_REMOTE = os.getenv("MONGODB_URI_REMOTE")
ID_SERVER = os.getenv("ID_SERVER")
SERVER_URL = os.getenv("SERVER_URL")

# Email configuration
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-email-password")

# JWT Secret key
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")