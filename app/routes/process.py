# backend/app/routes/process.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import fitz # PyMuPDF
from ..services.question_gen import generate_quiz_questions
from ..services.vocab_extractor import extract_vocabulary
from ..services.text_summarizer import summarize_text # Make sure this is imported

router = APIRouter()

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/generate-quiz/")
async def generate_quiz_endpoint(
    file: UploadFile = File(...),
    num_questions: int = Form(5),
    question_type: str = Form("multiple_choice"),
):
    print("--- Backend Debug: /generate-quiz/ endpoint received request ---")
    print(f"  Received file.filename: {file.filename}")
    print(f"  Received num_questions: {num_questions} (type: {type(num_questions)})")
    print(f"  Received question_type: {question_type} (type: {type(question_type)})")
    print("----------------------------------------------------")

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        # Save the uploaded PDF
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from PDF
        doc = fitz.open(file_location)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF. The PDF might be image-based or empty.")

        # Clean text (you might want to enhance this for better LLM input)
        cleaned_text = " ".join(text.split())

        # Generate questions
        questions = generate_quiz_questions(cleaned_text, num_questions, question_type)

        # Extract vocabulary
        vocabulary = extract_vocabulary(cleaned_text)


        response_content = {
            "questions": questions,
            "vocabulary": vocabulary,
        }

    except HTTPException as e:
        print(f"Error in /generate-quiz/: {e.detail}")
        raise e
    except Exception as e:
        print(f"Error generating quiz questions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz questions: {e}")
    finally:
        # Clean up the uploaded file
        if os.path.exists(file_location):
            os.remove(file_location)


@router.post("/extract-vocabulary/")
async def extract_vocabulary_endpoint(
    file: UploadFile = File(...),
    num_words: int = Form(10)
):
    print("--- Backend Debug: /extract-vocabulary/ endpoint received request ---")
    print(f"  Received file.filename: {file.filename}")
    print(f"  Received num_words: {num_words} (type: {type(num_words)})")
    print("----------------------------------------------------")

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc = fitz.open(file_location)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF. The PDF might be image-based or empty.")

        cleaned_text = " ".join(text.split())
        vocabulary = extract_vocabulary(cleaned_text, num_words)

        return JSONResponse(content={"vocabulary": vocabulary})

    except HTTPException as e:
        print(f"Error in /extract-vocabulary/: {e.detail}")
        raise e
    except Exception as e:
        print(f"Error extracting vocabulary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to extract vocabulary: {e}")
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)


@router.post("/summarize-text/")
async def summarize_text_endpoint(
    file: UploadFile = File(...),
    num_sentences: int = Form(3)
):
    print("--- Backend Debug: /summarize-text/ endpoint received request ---")
    print(f"  Received file.filename: {file.filename}")
    print(f"  Received num_sentences: {num_sentences} (type: {type(num_sentences)})")
    print("----------------------------------------------------")

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc = fitz.open(file_location)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF. The PDF might be image-based or empty.")

        cleaned_text = " ".join(text.split())
        summary = summarize_text(cleaned_text, num_sentences)

        return JSONResponse(content={"summary": summary})

    except HTTPException as e:
        print(f"Error in /summarize-text/: {e.detail}")
        raise e
    except Exception as e:
        print(f"Error summarizing text: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to summarize text: {e}")
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)