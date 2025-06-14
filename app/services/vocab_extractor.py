import os
import json
import re
from collections import Counter
from dotenv import load_dotenv

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from google.generativeai import GenerativeModel, configure

# Load environment variables
load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel('gemini-2.0-flash')

# Ensure required NLTK data is available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Prepare NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_and_tokenize(text):
    """Lowercase, remove punctuation/numbers, tokenize, filter stopwords, and lemmatize."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2]
    return tokens

def extract_vocabulary(text: str, num_words: int = 10) -> list:
    """
    Extracts important vocabulary words from text using NLP + Gemini API.
    Returns a list of dictionaries with word, definition, and part of speech.
    """
    if not text:
        return []

    tokens = clean_and_tokenize(text)
    if not tokens:
        return []

    word_counts = Counter(tokens)
    min_count = 2
    max_frequency_ratio = 0.05
    total_tokens = len(tokens)

    meaningful_words = [
        word for word, count in word_counts.most_common()
        if count >= min_count and (count / total_tokens) <= max_frequency_ratio
    ][:num_words * 2]

    if len(meaningful_words) < num_words:
        meaningful_words = [word for word, _ in word_counts.most_common(num_words * 2)]

    if not meaningful_words:
        return []

    prompt = f"""
    Given the following text, identify the {num_words} most important and relevant vocabulary words from this list: {', '.join(meaningful_words)}.
    For each word, provide a concise definition and its part of speech.

    Format the result as a JSON array like this:
    [
      {{
        "word": "Example",
        "definition": "A brief explanation of the word.",
        "part_of_speech": "noun"
      }},
      ...
    ]

    Text to analyze:
    {text[:2000]}
    """

    try:
        response = model.generate_content(prompt)
        vocab_json_string = response.text.strip()

        # Remove markdown formatting if present
        if vocab_json_string.startswith("```json"):
            vocab_json_string = vocab_json_string[len("```json"):].strip()
        if vocab_json_string.endswith("```"):
            vocab_json_string = vocab_json_string[:-len("```")].strip()

        vocabulary = json.loads(vocab_json_string)

        if not isinstance(vocabulary, list):
            print(f"Warning: Expected list from Gemini but got: {type(vocabulary)}")
            return []

        filtered = [
            item for item in vocabulary
            if isinstance(item, dict)
            and item.get('word')
            and item.get('definition')
            and item.get('part_of_speech')
        ]

        return filtered[:num_words]

    except Exception as e:
        print(f"Error extracting vocabulary: {e}")
        if 'response' in locals():
            print(f"Gemini response (if available): {response.text[:500]}")
        return []
