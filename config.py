import os
from dotenv import load_dotenv

# Load .env into environment
load_dotenv()

# Flask
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

# MongoDB (full URI, e.g. mongodb+srv://user:pass@cluster0/mydb)
MONGO_URI = os.getenv("MONGO_URI")

# File uploads
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
