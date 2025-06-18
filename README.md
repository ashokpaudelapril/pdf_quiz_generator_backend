# PDF Quiz Generator Backend

This is the backend API for the PDF Quiz Generator project. It provides endpoints to extract text from PDF files, generate quiz questions, extract vocabulary, and summarize text using Google Gemini AI models.

## Features

- **Quiz Generation:** Generate multiple-choice and true/false questions from PDF content.
- **Vocabulary Extraction:** Extract key vocabulary words with definitions and parts of speech.
- **Text Summarization:** Summarize PDF content into a specified number of sentences.
- **REST API:** FastAPI-based endpoints for easy integration with the frontend.
- **PDF Text Extraction:** Uses PyMuPDF for robust PDF parsing.

## Project Structure

```
backend/
  app/
    __init__.py
    main.py
    config.py
    routes/
      process.py
    services/
      question_gen.py
      vocab_extractor.py
      text_summarizer.py
      pdf_reader.py
    utils/
      text_cleaner.py
  tests/
    test_question_gen.py
  uploaded_files/
  uploaded_pdfs/
  requirements.txt
  .env
  README.md
```

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/ashokpaudelapril/pdf_quiz_generator_backend
```

### 2. Create and Activate a Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the `backend/` directory with the following content:

```
GEMINI_API_KEY=your_google_gemini_api_key
FRONTEND_URL=http://localhost:5173
```

- Replace `your_google_gemini_api_key` with your actual Gemini API key.
- Adjust `FRONTEND_URL` as needed for deployment.

### 5. Download NLTK Data (Optional)

The backend will attempt to download required NLTK data (`punkt`, `wordnet`, `omw-1.4`) on startup. If you encounter issues, you can manually download them:

```sh
python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('wordnet')
>>> nltk.download('omw-1.4')
```

### 6. Run the Backend Server

```sh
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

- `POST /api/generate-quiz/`  
  Upload a PDF and generate quiz questions and vocabulary.

- `POST /api/extract-vocabulary/`  
  Upload a PDF and extract vocabulary words.

- `POST /api/summarize-text/`  
  Upload a PDF and get a summary.

- `GET /api/health`  
  Health check endpoint.


## Notes

- Uploaded files are stored temporarily in `uploaded_pdfs/` and deleted after processing.
- Make sure your Google Gemini API key is valid and has sufficient quota.
- For production, configure CORS and environment variables appropriately.

## License

MIT License

---

For questions or contributions, please open an issue or pull request on the [GitHub repository](https://github.com/ashokpaudelapril/pdf_quiz_generator_backend).