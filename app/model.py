from app import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

class TestQuestion(db.Model):
    id = db.Column(db.String, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    document = db.relationship('Document', backref=db.backref('test_questions', lazy=True))
