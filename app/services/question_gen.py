# backend/app/services/question_gen.py

from google.generativeai import GenerativeModel, configure
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

configure(api_key=os.getenv("GEMINI_API_KEY"))
# Ensure you are using the correct, available model here
# (e.g., 'gemini-1.5-pro' or 'gemini-1.0-pro')
model = GenerativeModel('gemini-1.5-pro') # Using gemini-1.5-pro as an example

def generate_quiz_questions(text: str, num_questions: int, question_type: str) -> list:
    if not text:
        return []

    # Clean text to remove excessive whitespace which can confuse LLMs
    cleaned_text = " ".join(text.split())

    # Adjust num_questions for the prompt to allow for some filtering
    # Requesting slightly more questions to ensure we get enough valid ones after parsing/filtering.
    prompt_num_questions = num_questions + 2 # Request 2 more than needed

    if question_type == "multiple_choice":
        prompt = f"""
        Generate {prompt_num_questions} {question_type.replace('_', ' ')} questions about the following text.
        For each question, provide 4 options (A, B, C, D), indicating the correct answer.
        Crucially, for each question, provide a concise **'explanation'** (as a string) that elaborates on why the correct answer is right or provides additional context. This explanation should be directly related to the question and its answer.
        The output MUST be a JSON array of objects. Each object MUST have 'question' (string), 'options' (an array of 4 strings), 'answer' (the correct option string), 'type' (always 'multiple_choice'), and **'explanation'** (a string).

        Example JSON structure:
        [
          {{
            "question": "What is the capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "answer": "Paris",
            "type": "multiple_choice",
            "explanation": "Paris is the capital and most populous city of France, known globally for its art, fashion, and culture. It's a major center for international diplomacy and business."
          }},
          {{
            "question": "Which river flows through London?",
            "options": ["Seine", "Thames", "Danube", "Rhine"],
            "answer": "Thames",
            "type": "multiple_choice",
            "explanation": "The River Thames is a river that flows through southern England, most notably through London. It is the longest river entirely in England and the second longest in the United Kingdom."
          }}
        ]

        Text to generate questions from:
        {cleaned_text[:8000]} # Limit text length for prompt to manage token count
        """
    elif question_type == "true_false":
        prompt = f"""
        Generate {prompt_num_questions} {question_type.replace('_', ' ')} questions about the following text.
        For each question, the answer should be either "True" or "False".
        Crucially, for each question, provide a concise **'explanation'** (as a string) that elaborates on why the answer is correct or provides additional context.
        The output MUST be a JSON array of objects. Each object MUST have 'question' (string), 'answer' ("True" or "False" string), 'type' (always 'true_false'), and **'explanation'** (a string).

        Example JSON structure:
        [
          {{
            "question": "The Earth is flat.",
            "answer": "False",
            "type": "true_false",
            "explanation": "The Earth is an oblate spheroid, meaning it is a sphere flattened at the poles and bulging at the equator, a fact confirmed by extensive scientific observation and space travel."
          }},
          {{
            "question": "Photosynthesis is the process by which plants convert light energy into chemical energy.",
            "answer": "True",
            "type": "true_false",
            "explanation": "Photosynthesis is a vital process occurring in green plants, algae, and some bacteria, using sunlight to synthesize foods with the help of chlorophyll, carbon dioxide, and water."
          }}
        ]

        Text to generate questions from:
        {cleaned_text[:8000]} # Limit text length for prompt
        """
    else:
        raise ValueError("Unsupported question type. Only 'multiple_choice' and 'true_false' are supported.")

    try:
        response = model.generate_content(prompt)
        # Assuming response.text might include markdown code block delimiters
        json_string = response.text.strip()
        if json_string.startswith("```json"):
            json_string = json_string[len("```json"):].strip()
        if json_string.endswith("```"):
            json_string = json_string[:-len("```")].strip()

        questions_json = json.loads(json_string)

        if not isinstance(questions_json, list):
            print(f"Warning: Gemini response was not a list for questions: {json_string[:200]}...")
            return []

        # Filter out questions that don't match the requested type or are malformed
        # Ensure 'explanation' field is present during validation
        filtered_questions = []
        for q in questions_json:
            if isinstance(q, dict) and q.get('question') and q.get('answer') and q.get('type') == question_type and q.get('explanation') is not None:
                if question_type == 'multiple_choice':
                    if isinstance(q.get('options'), list) and len(q['options']) == 4:
                        filtered_questions.append(q)
                else: # For true_false
                    filtered_questions.append(q)
            else:
                print(f"Skipping malformed or mismatched question: {q}")
        
        # Return only up to the requested number of questions
        return filtered_questions[:num_questions]

    except Exception as e:
        print(f"Error generating quiz questions: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Raw Gemini response text (if available): {response.text}")
        return []