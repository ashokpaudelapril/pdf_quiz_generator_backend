from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys
import nltk

# Print the Python version that is running this script
print(f"--- Backend Running with Python: {sys.version} ---") # ADD THIS LINE
print(f"--- Executable path: {sys.executable} ---") # ADD THIS LINE


# Import your routers
from .routes import process

# Load environment variables from .env file
load_dotenv()



app = FastAPI(
    title="PDF Quiz & Vocabulary Generator API",
    description="API for extracting text from PDFs, generating quizzes, and extracting vocabulary.",
    version="1.0.0"
)


# Get allowed origins from environment variable or default to localhost for local dev
# In Render, you will set FRONTEND_URL to your deployed frontend URL (e.g., https://your-frontend.vercel.app)
allowed_origins = os.getenv("FRONTEND_URL", "http://localhost:5173").split(",")
# Add common localhost origins for local testing
allowed_origins.append("http://localhost:3000") # React default
allowed_origins.append("http://localhost:5173") # Vite default
allowed_origins.append("http://127.0.0.1:8000") # FastAPI default
allowed_origins.append("http://localhost:8000") # FastAPI default


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins, # This list contains the actual URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routers
app.include_router(process.router, prefix="/api", tags=["generation"])

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint to verify backend is running.
    """
    return {"status": "ok", "message": "Backend is running!"}

# 👇 ADD THIS FASTAPI STARTUP HANDLER
@app.on_event("startup")
async def download_nltk_data():
    print("--- Checking for required NLTK resources ---")
    nltk.data.path.append("/opt/render/nltk_data")
    for resource in ["punkt", "wordnet", "omw-1.4"]:
        try:
            nltk.data.find(resource)
            print(f"✓ Found: {resource}")
        except LookupError:
            print(f"⬇ Downloading: {resource}")
            nltk.download(resource, download_dir="/opt/render/nltk_data")

if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 to make it accessible from outside the container in Docker setups
    uvicorn.run(app, host="0.0.0.0", port=8000)