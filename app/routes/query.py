from flask import Blueprint, request, jsonify
from app.model import Document, TestQuestion
from app import db
import spacy
import random

# Initialize spaCy NLP model
nlp = spacy.load('en_core_web_md')

bp = Blueprint('query', __name__, url_prefix='/query')

def extract_context_with_keywords(document_content, question, keywords=None, n_sentences=5):
    """
    Extract context that is most relevant to the question based on keywords.
    """
    # Define default keywords if none are provided
    if keywords is None:
        keywords = ["ethical", "concerns", "privacy", "bias", "transparency"]

    # Process document content using spaCy
    doc = nlp(document_content)

    # Split the document into paragraphs or sentences
    paragraphs = [p.text for p in doc.sents if any(kw in p.text.lower() for kw in keywords)]

    # If relevant paragraphs are found, join them to form a new context
    if paragraphs:
        context = " ".join(paragraphs)
    else:
        # Fall back to full document content if no keywords match
        context = document_content

    # Further refine the context by finding sentences that match the question
    refined_context = extract_context(context, question, n_sentences=n_sentences)
    return refined_context

def extract_context(document_content, question, n_sentences=5):
    """
    Find the most relevant sentences around the question context.
    """
    doc = nlp(document_content)
    # Find sentences similar to the question
    sentences = list(doc.sents)
    # Get the best matching sentence based on similarity to the question
    best_sentence = max(sentences, key=lambda sent: sent.similarity(nlp(question)))

    # Get n_sentences around the best match for better context
    best_index = sentences.index(best_sentence)
    start_index = max(0, best_index - n_sentences // 2)
    end_index = min(len(sentences), best_index + n_sentences // 2 + 1)

    # Return the context string
    return " ".join([str(sent) for sent in sentences[start_index:end_index]])

def generate_answer(content, question):
    # Extract relevant context with a focus on keywords
    context = extract_context_with_keywords(content, question)
    
    # Use the spaCy similarity-based approach to extract an answer from the context
    doc_content = nlp(context)
    doc_question = nlp(question)

    # Find sentences in the context similar to the question
    sentences = [sent for sent in doc_content.sents]
    best_sentence = max(sentences, key=lambda sent: sent.similarity(doc_question))

    # Extract the best matching sentence as the answer
    answer = best_sentence.text

    # Generate up to 3 bullet points by splitting the answer into sentences or phrases
    bullet_points = [str(sent).strip() for sent in list(nlp(answer).sents)[:3]]  # Convert to list before slicing

    return answer, bullet_points


def generate_test_question(answer):
    # Generate a simple test question based on the answer
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

    # Generate answer and bullet points using refined context
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

    # Format response with new lines for better readability
    return jsonify({
        "answer": answer,
        "bullet_points": "\n\n".join(bullet_points),  # Add new lines between bullet points
        "test_question": test_question,
        "test_question_id": test_question_id
    })
