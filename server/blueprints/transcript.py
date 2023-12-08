from flask import Blueprint, jsonify, request, current_app
from concurrent.futures import ThreadPoolExecutor
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Transcript, TransHistory, db
from controller.transcriptController import create_task

transcript = Blueprint('transcript', __name__)
executor = ThreadPoolExecutor(5)

@transcript.route('/list', methods=['GET'])
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
        transcripts = Transcript.query.filter_by(user_id=user_id).all()
        # convert to json
        response_object['data'] = [t.to_dict() for t in transcripts]
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
def create_transcript():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    # check if all data is provided
    title = post_data.get('title')
    content = post_data.get('content')
    task = post_data.get('type')
    audio_name = post_data.get('audio_name')
    user_id = get_jwt_identity()

    if not title or (not content and not audio_name) or not task:
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
            audio_name = audio_name
        )
        db.session.add(transcript)
        db.session.commit()
        response_object['msg'] = 'Create transcript successfully'
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    # create task
    executor.submit(create_task, transcript.id)

    return jsonify(response_object)

@transcript.route('/update', methods=['POST'])
@jwt_required()
def update_transcript():
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
            status = transcript.status,
            audio_path = transcript.audio_path
        )
        transcript.title = title
        transcript.content = content
        transcript.task = task
        transcript.audio_path = audio_path
        transcript.status = "Running"
        transcript.analysis = None

        db.session.add(history)
        db.session.commit()

        response_object['msg'] = 'Update transcript successfully'
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    return jsonify(response_object)

# delete transcript, need to cancel the task first???
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
        db.session.delete(transcript)
        db.session.commit()
        response_object['msg'] = 'Delete transcript successfully'
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
        return jsonify(response_object), 400
    
    return jsonify(response_object)