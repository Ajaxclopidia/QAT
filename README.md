# QAT
Building a Q.A.T (Question, Answer &amp; Test) system for research documents.

Q.A.T System
A Question Answering and Testing (Q.A.T) System that allows users to upload documents, ask questions based on the uploaded content, receive answers with bullet points, generate test questions, and evaluate user responses.

Table of Contents
Introduction
Features
Demo Video
Installation
Prerequisites
Clone the Repository
Create a Virtual Environment
Install Dependencies
Download SpaCy Model
Usage
Running the Application
Accessing the Application
Using the Application
Project Structure
License
Contact
Introduction
The Q.A.T System is a web application that allows users to:

Upload text-based documents.
Ask questions related to the content of the uploaded documents.
Receive comprehensive answers along with bullet points summarizing key points.
Generate test questions based on the answers.
Evaluate user responses to the test questions for understanding and confidence.
This application leverages Natural Language Processing (NLP) techniques and models to process text and generate meaningful interactions.

Features
Document Upload: Supports uploading of text files to be stored and queried.
Question Answering: Provides answers to user questions based on the uploaded documents.
Bullet Point Extraction: Summarizes answers into key bullet points for better understanding.
Test Question Generation: Generates relevant test questions from the answers.
Response Evaluation: Evaluates user answers to test questions and provides feedback on understanding and confidence level.
Responsive UI: A user-friendly interface built with Bootstrap for ease of use.
Demo Video
Watch the Demo Video <!-- -->

Note: Please click on the link above to watch a demonstration of the Q.A.T System in action.

Installation
Follow these steps to set up and run the application locally.

Prerequisites
Python 3.8 or higher
pip (Python package installer)
git (to clone the repository)
Clone the Repository
Open your terminal or command prompt and run:

bash
Copy code
git clone https://github.com/yourusername/qat-system.git
cd qat-system
Replace yourusername with your GitHub username.

Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy code
venv\Scripts\activate
On macOS/Linux:

bash
Copy code
source venv/bin/activate
Install Dependencies
Install the required Python packages using requirements.txt:

bash
Copy code
pip install -r requirements.txt
Download SpaCy Model
Download the English SpaCy model:

bash
Copy code
python -m spacy download en_core_web_sm
This model is necessary for NLP tasks within the application.

Usage
Running the Application
Set the Flask application environment variables:

bash
Copy code
export FLASK_APP=run.py
export FLASK_ENV=development
On Windows, use set instead of export.

Initialize the database:

bash
Copy code
python run.py db init
python run.py db migrate
python run.py db upgrade
Run the Flask application:

bash
Copy code
flask run
The application will start running at http://localhost:5001.

Accessing the Application
Open your web browser and navigate to http://localhost:5001 to access the Q.A.T System interface.

Using the Application
1. Upload Document
Click on "Upload Document".
Choose a text file (.txt) from your computer.
Click "Upload".
Note the Document ID provided after a successful upload.
2. Query Document
Navigate to the "Query Document" section.
Enter the Document ID of the uploaded document.
Enter your Question related to the document's content.
Click "Query".
View the Answer, Bullet Points, Test Question, and Test Question ID.
3. Evaluate Response
Go to the "Evaluate Response" section.
Enter the Test Question ID obtained from the previous step.
Provide your Answer to the test question.
Click "Evaluate".
Receive feedback on Knowledge Understood and Knowledge Confidence.
Project Structure
arduino
qat-system/
├── app/
│   ├── __init__.py
│   ├── model.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   ├── query.py
│   │   └── evaluate.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       └── js/
├── run.py
├── requirements.txt
├── README.md
└── .gitignore
app/: Contains the main application modules.
model.py: Defines the database models.
routes/: Contains the route handlers for different endpoints.
templates/: Contains the HTML templates.
static/: Contains static files like CSS and JavaScript.
run.py: The main entry point to run the Flask application.
requirements.txt: Lists all Python dependencies.
README.md: Documentation for the project.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any questions or feedback, please contact:

Name: Muhammed Ajasa
Email: ajaxclopidia77@gmail.com
Feel free to customize the above template according to your project's specifics. Below are additional details you might want to include:

Screenshots: Add screenshots of the application to visually demonstrate its features.

markdown
## Screenshots

![Upload Document](screenshots/upload_document.png)

*Caption: Uploading a document.*

![Query Document](screenshots/query_document.png)

*Caption: Querying the document and viewing the answer.*
Technologies Used: List the key technologies and libraries used in the project.

markdown
## Technologies Used

- **Python 3.8**
- **Flask**: Web framework for Python.
- **SpaCy**: For natural language processing tasks.
- **SentenceTransformers**: For semantic similarity and embeddings.
- **Transformers**: For leveraging pre-trained NLP models.
- **Bootstrap**: For responsive UI design.
- **SQLite**: As the database for storing documents and test questions.
Contributing: Instructions on how others can contribute to your project.

markdown
## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.
Acknowledgments: Credit any resources or inspirations that helped in the project.

markdown
## Acknowledgments

- [OpenAI GPT-4](https://openai.com/research/gpt-4)
- [SpaCy Documentation](https://spacy.io/usage)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Bootstrap](https://getbootstrap.com/)
FAQ: Answer common questions that users might have.

markdown
## FAQ

**Q:** Can I upload documents in formats other than `.txt`?

**A:** Currently, the system supports only text files (`.txt`). Support for other formats may be added in future updates.
