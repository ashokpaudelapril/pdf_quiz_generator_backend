from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

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

# Configure CORS
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"), # For CRA
    os.getenv("FRONTEND_URL_VITE", "http://localhost:5173"), # For Vite
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods
    allow_headers=["*"], # Allows all headers
)

# Include your API routers
app.include_router(process.router, prefix="/api", tags=["generation"])

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint to verify backend is running.
    """
    return {"status": "ok", "message": "Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 to make it accessible from outside the container in Docker setups
    uvicorn.run(app, host="0.0.0.0", port=8000)