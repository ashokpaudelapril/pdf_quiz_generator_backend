# backend/app/config.py
import os

# Define a directory to temporarily store uploaded files
# Ensure this directory exists or is created when the app starts
UPLOAD_DIR = os.path.join(os.getcwd(), "uploaded_files")

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# You can add other configurations here, e.g., default number of questions, etc.
DEFAULT_NUM_QUESTIONS = 5
DEFAULT_QUESTION_TYPE = "multiple_choice"