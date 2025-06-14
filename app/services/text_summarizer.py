# backend/app/services/text_summarizer.py
from google.generativeai import GenerativeModel, configure
import os
from dotenv import load_dotenv

load_dotenv()

configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel('gemini-2.0-flash')

def summarize_text(text: str, num_sentences: int = 3) -> str:
    """
    Summarizes the given text into a specified number of sentences using Gemini API.

    Args:
        text (str): The text content to summarize.
        num_sentences (int): The desired number of sentences for the summary.

    Returns:
        str: The generated summary.
    """
    if not text:
        return ""

    # Limit text length for the prompt to avoid token limits
    # A typical prompt + 2000 chars should be safe for most models
    text_for_prompt = text[:4000] # Adjust based on typical document length and model context window

    prompt = f"""
    Summarize the following text concisely into approximately {num_sentences} sentences.
    Focus on the main points and key information.

    Text to summarize:
    {text_for_prompt}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error summarizing text: {e}")
        # Print the raw response text for debugging
        if 'response' in locals():
            print(f"Raw Gemini response text (if available): {response.text}")
        return "Failed to generate summary."