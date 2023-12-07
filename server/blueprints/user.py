from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token
from models import User, Transcript, TransHistory, db

user = Blueprint('user', __name__)

@user.route('/create', methods=['POST'])
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
    user = User.query.filter_by(username=username).first()
    if user:
        response_object['msg'] = 'User already exists'
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
        response_object['msg'] = 'User created!'
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
    token = create_access_token(identity=username)
    response_object['token'] = token
    return jsonify(response_object)