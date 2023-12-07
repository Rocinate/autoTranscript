from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models import User, Transcript, TransHistory, db

user = Blueprint('user', __name__)

@user.route('/checkEmail', methods=['GET'])
def check_email():
    response_object = {'status': 'success'}
    email = request.args.get('email')

    # check if email exists
    user = User.query.filter_by(email=email).first()
    if user:
        response_object['msg'] = 'Email already exists'
        response_object['status'] = 'fail'
        return jsonify(response_object), 200

    return jsonify(response_object)

@user.route('/signup', methods=['POST'])
def create_user():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    # check if all data is provided
    username = post_data.get('username')
    password = post_data.get('password')
    email = post_data.get('email')

    if not username or not password or not email:
        response_object['msg'] = 'Invalid payload'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400

    # check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        response_object['msg'] = 'email already exists'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400

    # add user to database
    try:
        db.session.add(User(
            username = username,
            password = password,
            email = email,
        ))
        db.session.commit()

        # generate token
        token = create_access_token(identity=user.id)
        response_object['msg'] = 'User created!'
        response_object['token'] = token
        return jsonify(response_object)
    except Exception as e:
        response_object['msg'] = str(e)
        response_object['status'] = 'fail'
    return jsonify(response_object)

@user.route('/login', methods=['POST'])
def login():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    # check if all data is provided
    username = post_data.get('username')
    password = post_data.get('password')

    if not username or not password:
        response_object['msg'] = 'Invalid payload'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400

    # check if user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        response_object['msg'] = 'User does not exist'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400

    # check if password is correct
    if not user.check_password(password):
        response_object['msg'] = 'Wrong password'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400

    # generate token
    token = create_access_token(identity=user.id)
    response_object['token'] = token
    return jsonify(response_object)

@user.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    response_object = {'status': 'success'}
    user_id = get_jwt_identity()

    # check if user exists
    user = User.query.filter_by(id=user_id).first()
    if not user:
        response_object['msg'] = 'User does not exist'
        response_object['status'] = 'fail'
        return jsonify(response_object), 400

    response_object['username'] = user.username
    response_object['email'] = user.email
    response_object['require_times'] = user.require_times
    response_object['transcription_count'] = user.transcription_count
    response_object['registered_on'] = user.registered_on.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(response_object)