from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from functools import wraps
import os

app = Flask(__name__)
CORS(app)

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Define your bearer token
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

# Decorator to require bearer token
def require_bearer_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        token = auth.split('Bearer ')[1]
        if token != BEARER_TOKEN:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/parse', methods=['POST'])
@require_bearer_token
def parse_text():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    doc = nlp(text)

    result = []
    for token in doc:
        token_data = {
            'text': token.text,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'dep': token.dep_,
            'head': token.head.text,
            'children': [child.text for child in token.children]
        }
        result.append(token_data)

    return jsonify(result)
