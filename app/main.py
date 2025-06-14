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


# Get allowed origins from environment variable or default to localhost for local dev
# In Render, you will set FRONTEND_URL to your deployed frontend URL (e.g., https://your-frontend.onrender.com)
allowed_origins = os.getenv("FRONTEND_URL", "http://localhost:5173").split(",")
# Add localhost for local testing (React default dev server is 5173 or 3000)
allowed_origins.append("http://localhost:3000") # React default
allowed_origins.append("http://localhost:5173") # Vite default
allowed_origins.append("http://127.0.0.1:8000") # FastAPI default
allowed_origins.append("http://localhost:8000") # FastAPI default


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins, # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
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