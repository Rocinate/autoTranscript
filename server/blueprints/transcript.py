import asyncio
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Transcript, TransHistory, db
from controller.transcript import create_task

transcript = Blueprint('transcript', __name__)

@transcript.route('/get', methods=['GET'])
@jwt_required()
def get_task_list():
    response_object = {'status': 'success'}
    user_id = get_jwt_identity()

    # check if user exists
    user = User.query.filter_by(id=user_id).first()
    if not user:
        response_object['msg'] = 'User does not exist'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # get task list
    try:
        transcript = Transcript.query.filter_by(user_id=user_id).all()
        response_object['transcript'] = transcript
        response_object['msg'] = 'Get task list successfully'
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
        return jsonify(response_object), 400

    return jsonify(response_object)

@transcript.route('/detail', methods=['GET'])
@jwt_required()
def get_task_detail():
    response_object = {'status': 'success'}
    user_id = get_jwt_identity()

    # check if user exists
    user = User.query.filter_by(id=user_id).first()
    if not user:
        response_object['msg'] = 'User does not exist'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # get task detail
    try:
        transcript_id = request.args.get('id')
        transcript = Transcript.query.filter_by(id=transcript_id).first()

        # get all history
        history = TransHistory.query.filter_by(parent_id=transcript_id).all()
        transcript.history = history

        response_object['transcript'] = transcript
        response_object['msg'] = 'Get task detail successfully'
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
        return jsonify(response_object), 400

    return jsonify(response_object)


@transcript.route('/create', methods=['POST'])
@jwt_required()
async def create_transcript():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    # check if all data is provided
    title = post_data.get('title')
    content = post_data.get('content')
    task = post_data.get('task')
    audio_path = post_data.get('audio_path')
    user_id = get_jwt_identity()

    if not title or (not content and not audio_path) or not task:
        response_object['msg'] = 'Invalid payload'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # check if user exists
    user = User.query.filter_by(id=user_id).first()
    if not user:
        response_object['msg'] = 'User does not exist'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # create transcript
    try:
        transcript = Transcript(
            title = title,
            content = content,
            task = task,
            user_id = user_id,
            audio_path = audio_path
        )
        db.session.add(transcript)
        db.session.commit()
        response_object['msg'] = 'Create transcript successfully'
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # create task
    asyncio.run(create_task(transcript))

    return jsonify(response_object)
    

@transcript.route('/update', methods=['POST'])
@jwt_required()
async def update_transcript():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    # check if all data is provided
    transcript_id = post_data.get('id')
    title = post_data.get('title')
    content = post_data.get('content')
    task = post_data.get('task')
    audio_path = post_data.get('audio_path')
    user_id = get_jwt_identity()

    if not transcript_id or not title or (not content and not audio_path) or not task:
        response_object['msg'] = 'Invalid payload'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # check if user exists、
    user = User.query.filter_by(id=user_id).first()
    if not user:
        response_object['msg'] = 'User does not exist'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # check if transcript exists
    transcript = Transcript.query.filter_by(id=transcript_id).first()
    if not transcript:
        response_object['msg'] = 'Transcript does not exist'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # create history and update transcript
    try:
        history = TransHistory(
            parent_id = transcript_id,
            title = transcript.title,
            content = transcript.content,
            analysis = transcript.analysis,
            task = transcript.task,
            user_id = transcript.user_id,
            finished = transcript.finished,
            video_path = transcript.video_path,
            audio_path = transcript.audio_path
        )
        transcript.title = title
        transcript.content = content
        transcript.task = task
        transcript.audio_path = audio_path
        transcript.finished = False
        transcript.analysis = None
        db.session.commit()

        response_object['msg'] = 'Update transcript successfully'
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    return jsonify(response_object)


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
        transcript.delete()
        db.session.commit()
        response_object['msg'] = 'Delete transcript successfully'
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    return jsonify(response_object)