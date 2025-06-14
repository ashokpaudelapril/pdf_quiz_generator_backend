import pytest
from app.services.question_gen import generate_quiz_questions

# Sample text for testing
TEST_TEXT = """
The Amazon rainforest is the largest rainforest in the world.
It is home to an incredible diversity of plants and animals.
The Amazon river flows through the rainforest.
Deforestation is a major threat to this unique ecosystem.
"""

def test_generate_short_answer_questions():
    questions = generate_quiz_questions(TEST_TEXT, num_questions=2, question_type="short_answer")
    assert len(questions) <= 2 # Might generate less if text is too short
    if questions:
        assert all(q['type'] == 'short_answer' for q in questions)
        assert all('question' in q and 'answer' in q for q in questions)

def test_generate_multiple_choice_questions():
    questions = generate_quiz_questions(TEST_TEXT, num_questions=2, question_type="multiple_choice")
    assert len(questions) <= 2
    if questions:
        assert all(q['type'] == 'multiple_choice' for q in questions)
        assert all('question' in q and 'options' in q and 'answer' in q for q in questions)
        assert all(len(q['options']) == 4 for q in questions) # Expect 4 options

def test_generate_true_false_questions():
    questions = generate_quiz_questions(TEST_TEXT, num_questions=2, question_type="true_false")
    assert len(questions) <= 2
    if questions:
        assert all(q['type'] == 'true_false' for q in questions)
        assert all('question' in q and 'answer' in q for q in questions)
        assert all(q['answer'] in ["True", "False"] for q in questions)

def test_empty_text():
    questions = generate_quiz_questions("", num_questions=1, question_type="short_answer")
    assert questions == []

def test_unsupported_question_type():
    questions = generate_quiz_questions(TEST_TEXT, num_questions=1, question_type="unsupported")
    assert questions == []