from flask import Blueprint, request, jsonify
from app.model import TestQuestion
import spacy
import logging

# Use a unique name for the blueprint to avoid conflicts
bp = Blueprint('evaluate', __name__, url_prefix='/evaluate')

# Load spaCy model for semantic similarity
nlp = spacy.load('en_core_web_md')

def calculate_similarity(text1, text2):
    # Process texts with spaCy
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    
    # Calculate similarity score
    similarity_score = doc1.similarity(doc2)
    
    return similarity_score

def evaluate_user_response(user_answer, correct_answer):
    # Calculate semantic similarity
    similarity_score = calculate_similarity(user_answer, correct_answer)
    
    # Calculate keyword overlap
    correct_keywords = set(correct_answer.lower().split()) - set(nlp.Defaults.stop_words)
    user_keywords = set(user_answer.lower().split()) - set(nlp.Defaults.stop_words)
    keyword_overlap = len(correct_keywords.intersection(user_keywords)) / len(correct_keywords) if correct_keywords else 0
    
    # Combine scores (you can adjust weights as needed)
    combined_score = (similarity_score * 0.7) + (keyword_overlap * 0.3)
    
    # Dynamic thresholding based on answer complexity
    threshold = 0.6 if len(correct_answer.split()) > 20 else 0.7
    
    understood = combined_score > threshold
    confidence = int(combined_score * 100)

    return understood, confidence

@bp.route('/', methods=['POST'])
def evaluate_response():
    data = request.json
    user_answer = data.get('user_answer', '').strip()
    test_question_id = data.get('test_question_id')

    if not user_answer:
        return jsonify({"error": "User answer is empty"}), 400

    # Retrieve the correct answer for the test_question_id from the database
    test_question_record = TestQuestion.query.get(test_question_id)
    if not test_question_record:
        return jsonify({"error": "Test question not found"}), 404

    correct_answer = test_question_record.correct_answer

    # Evaluate the user's response
    knowledge_understood, knowledge_confidence = evaluate_user_response(user_answer, correct_answer)

    # Log the evaluation result
    logging.info(f"Evaluation for question {test_question_id}: Understood: {knowledge_understood}, Confidence: {knowledge_confidence}")

    return jsonify({
        "knowledge_understood": knowledge_understood,
        "knowledge_confidence": knowledge_confidence
    })