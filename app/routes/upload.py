from flask import Blueprint, request, jsonify
from app.model import Document
from app import db

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/', methods=['POST'])
def upload_document():
    # Expecting the document to be sent as a file in the POST request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    
    # Read the content and filename of the document
    content = file.read().decode('utf-8')  # Assuming the file is text-based
    title = file.filename
    
    # Save document content to the database
    document = Document(title=title, content=content)
    db.session.add(document)
    db.session.commit()

    return jsonify({"message": "Document uploaded successfully", "document_id": document.id})
