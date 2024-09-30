from flask import Blueprint, request, jsonify
from app.model import TestQuestion
import torch
from transformers import AutoTokenizer, AutoModel

# Use a unique name for the blueprint to avoid conflicts
bp = Blueprint('evaluate', __name__, url_prefix='/evaluate')

# Load a transformer model for semantic similarity
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

def calculate_similarity(text1, text2):
    # Tokenize and encode the texts
    tokens1 = tokenizer(text1, return_tensors='pt')
    tokens2 = tokenizer(text2, return_tensors='pt')
    
    # Get embeddings from the model
    with torch.no_grad():
        embeddings1 = model(**tokens1).last_hidden_state.mean(dim=1)
        embeddings2 = model(**tokens2).last_hidden_state.mean(dim=1)
    
    # Calculate cosine similarity
    similarity = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)
    
    return similarity.item()

def evaluate_user_response(user_answer, correct_answer):
    # Calculate similarity score
    similarity_score = calculate_similarity(user_answer, correct_answer)
    
    # Set a threshold for understanding
    understood = similarity_score > 0.7  # Use a threshold to define understanding
    confidence = int(similarity_score * 100)  # Confidence as a percentage

    return understood, confidence

@bp.route('/', methods=['POST'])
def evaluate_response():
    data = request.json
    user_answer = data.get('user_answer')
    test_question_id = data.get('test_question_id')

    # Retrieve the correct answer for the test_question_id from the database
    test_question_record = TestQuestion.query.get(test_question_id)
    if not test_question_record:
        return jsonify({"error": "Test question not found"}), 404

    correct_answer = test_question_record.correct_answer

    # Evaluate the user's response
    knowledge_understood, knowledge_confidence = evaluate_user_response(user_answer, correct_answer)

    return jsonify({
        "knowledge_understood": knowledge_understood,
        "knowledge_confidence": knowledge_confidence
    })
