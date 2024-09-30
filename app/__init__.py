import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')  # Explicitly set the templates folder
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qat_system.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    # Enable CORS for all routes to avoid cross-origin issues
    CORS(app)

    # Import and register blueprints (routes)
    from app.routes import upload, query, evaluate
    app.register_blueprint(upload.bp)
    app.register_blueprint(query.bp)
    app.register_blueprint(evaluate.bp)

    # Route to render a simple homepage
    @app.route('/')
    def home():
        return render_template('index.html')

    return app
