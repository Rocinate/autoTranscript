from openai import OpenAI
import asyncio
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Transcript, TransHistory, db

# client = OpenAI()

transcript = Blueprint('transcript', __name__)

@transcript.route('/create', methods=['POST'])
@jwt_required()
async def create_transcript():
    pass

@transcript.route('/update', methods=['POST'])
@jwt_required()
async def update_transcript():
    pass

@transcript.route('/delete', methods=['POST'])
@jwt_required()
def delete_transcript():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    # check if all data is provided
    transcript_id = post_data.get('id')

    if not transcript_id:
        response_object['msg'] = 'Invalid payload'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # check if transcript exists
    transcript = Transcript.query.filter_by(id=transcript_id).first()

    if not transcript:
        response_object['msg'] = 'Transcript does not exist'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # delete transcript
    try:
        pass
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
        return jsonify(response_object), 400