# backend/app/utils/text_cleaner.py
import re

def clean_text(text: str) -> str:
    """
    Performs basic cleaning on text extracted from PDF.
    - Removes extra whitespace.
    - Removes non-alphanumeric characters (keeping some punctuation).
    - Converts to lowercase (though question/vocab gen might do this too, good to have it here).
    """
    if not isinstance(text, str):
        return ""

    # Remove extra whitespace (multiple spaces, newlines, tabs)
    cleaned_text = re.sub(r'\s+', ' ', text).strip()

    # Optional: Remove special characters, keep alphanumeric and basic punctuation
    # Example: Keep letters, numbers, spaces, and . , ! ?
    # cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', cleaned_text)

    # Optional: Convert to lowercase (can be done in subsequent steps as well)
    # cleaned_text = cleaned_text.lower()

    return cleaned_text