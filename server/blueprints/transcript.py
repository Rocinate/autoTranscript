from openai import OpenAI
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Transcript, TransHistory, db

# client = OpenAI()

transcript = Blueprint('transcript', __name__)

@transcript.route('/audio', methods=['POST'])
def audio_to_text():
    pass

@transcript.route('/create', methods=['POST'])
def create_transcript():
    pass

@transcript.route('/update', methods=['POST'])
def update_transcript():
    pass

@transcript.route('/delete', methods=['POST'])
def delete_transcript():
    pass