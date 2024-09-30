from flask import Blueprint, request, jsonify
from app.model import Document, TestQuestion
from app import db
import spacy
import random

# Initialize spaCy NLP model
nlp = spacy.load('en_core_web_sm')

bp = Blueprint('query', __name__, url_prefix='/query')

def generate_answer(content, question):
    # Process the content and question using spaCy
    doc_content = nlp(content)
    doc_question = nlp(question)

    # Find sentences in the content similar to the question
    sentences = [sent for sent in doc_content.sents]
    best_sentence = max(sentences, key=lambda sent: sent.similarity(doc_question))

    # Extract the best matching sentence as the answer
    answer = best_sentence.text

    # Generate bullet points by splitting the answer into meaningful chunks
    bullet_points = [str(sent).strip() for sent in nlp(answer).sents]

    return answer, bullet_points

def generate_test_question(answer):
    # Generate a simple test question based on the answer
    # Here we use a basic heuristic: forming a question by rephrasing the answer
    test_question = f"What does the following statement imply: '{answer}'?"
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
