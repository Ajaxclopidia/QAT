from flask import Blueprint, request, jsonify
from app.model import Document, TestQuestion
from app import db
from transformers import pipeline
import random
from transformers import pipeline
import torch

# Check if MPS is available and set the device accordingly
device = 0 if torch.backends.mps.is_available() else -1

# Initialize the transformer pipelines
qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')
gpt_pipeline = pipeline('text-generation', model='gpt2')

bp = Blueprint('query', __name__, url_prefix='/query')

def generate_answer(content, question):
    # Use the QA pipeline to extract an answer from the content based on the question
    result = qa_pipeline(question=question, context=content)
    answer = result['answer']
    
    # Generate bullet points (for simplicity, we'll use key sentences in the answer)
    bullet_points = [answer]  # You can enhance this with more detailed analysis

    return answer, bullet_points

def generate_test_question(answer):
    # Use the GPT pipeline to generate a test question based on the answer
    prompt = f"Create a question to test the understanding of the following statement: {answer}"
    generated_text = gpt_pipeline(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']
    
    # Extract the test question from the generated text
    test_question = generated_text.replace(prompt, '').strip()
    test_question_id = f"tq_{random.randint(1000, 9999)}"

    return test_question, test_question_id

@bp.route('/', methods=['POST'])
def query_document():
    data = request.json
    document_id = data.get('document_id')
    question = data.get('question')

    # Retrieve the document
    document = Document.query.get(document_id)
    if not document:
        return jsonify({"error": "Document not found"}), 404

    content = document.content

    # Generate answer and bullet points
    answer, bullet_points = generate_answer(content, question)
    test_question, test_question_id = generate_test_question(answer)

    # Store test question and correct answer in the database
    test_question_record = TestQuestion(
        id=test_question_id,
        question=test_question,
        correct_answer=answer,  # Store the generated answer as the correct answer
        document_id=document_id
    )
    db.session.add(test_question_record)
    db.session.commit()

    return jsonify({
        "answer": answer,
        "bullet_points": bullet_points,
        "test_question": test_question,
        "test_question_id": test_question_id
    })