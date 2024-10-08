from flask import Blueprint, request, jsonify
from app.model import Document, TestQuestion
from app import db
import spacy
import random
from sentence_transformers import SentenceTransformer, util
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Sentence Transformer model for answer generation
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the tokenizer and model for question generation
tokenizer = AutoTokenizer.from_pretrained("valhalla/t5-small-qg-hl")
qg_model = AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-small-qg-hl")

bp = Blueprint('query', __name__, url_prefix='/query')

def generate_answer(content, question, top_k=3):
    # Split the content into sentences
    doc = nlp(content)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    
    # Encode the sentences and the question
    embeddings = sentence_model.encode(sentences, convert_to_tensor=True)
    question_embedding = sentence_model.encode(question, convert_to_tensor=True)
    
    # Compute cosine similarities
    cosine_scores = util.cos_sim(question_embedding, embeddings)[0]
    
    # Get the top_k most relevant sentences
    top_results = torch.topk(cosine_scores, k=top_k)
    
    # Combine the top sentences into the answer
    answer = ' '.join([sentences[idx] for idx in top_results.indices])
    
    return answer

def extract_bullet_points(answer, max_points=5):
    doc = nlp(answer)
    # Extract noun chunks (key phrases)
    phrases = [chunk.text.strip() for chunk in doc.noun_chunks if len(chunk.text.strip()) > 2]
    # Remove duplicates while preserving order
    seen = set()
    unique_phrases = []
    for phrase in phrases:
        if phrase.lower() not in seen:
            seen.add(phrase.lower())
            unique_phrases.append(phrase)
    # Sort phrases based on their order in the answer
    unique_phrases.sort(key=lambda x: answer.find(x))
    # Limit to max_points
    bullet_points = unique_phrases[:max_points]
    return bullet_points

def generate_test_question(answer):
    # Highlight key phrases in the answer using <hl> tags
    doc = nlp(answer)
    noun_chunks = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.strip()) > 2]
    if noun_chunks:
        # Highlight the first noun chunk for simplicity
        highlighted_phrase = noun_chunks[0]
        highlighted_answer = answer.replace(highlighted_phrase, f"<hl> {highlighted_phrase} <hl>", 1)
    else:
        # If no noun chunks, highlight the entire answer
        highlighted_answer = f"<hl> {answer} <hl>"
    
    # The model expects 'generate question: ' prefix
    input_text = f"generate question: {highlighted_answer}"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    
    # Generate the question using the model
    outputs = qg_model.generate(
        input_ids=input_ids,
        max_length=64,
        num_beams=5,
        early_stopping=True
    )
    
    # Decode the generated question
    question = tokenizer.decode(outputs[0], skip_special_tokens=True)
    test_question_id = f"tq_{random.randint(1000, 9999)}"
    return question, test_question_id

@bp.route('/', methods=['POST'])
def query_document():
    data = request.get_json()
    document_id = data.get('document_id')
    question = data.get('question')
    
    if not document_id or not question:
        return jsonify({"error": "document_id and question are required"}), 400

    document = Document.query.get(document_id)
    if not document:
        return jsonify({"error": "Document not found"}), 404

    content = document.content

    # Generate a comprehensive answer
    answer = generate_answer(content, question)

    # Extract bullet points from the answer
    bullet_points = extract_bullet_points(answer)

    # Generate a test question based on the answer
    test_question, test_question_id = generate_test_question(answer)

    # Store test question and correct answer in the database
    test_question_record = TestQuestion(
        id=test_question_id,
        question=test_question,
        correct_answer=answer,
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
