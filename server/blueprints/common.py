import os
from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from configs import UPLOAD_FOLDER
from utils import extract_audio

common = Blueprint("common", __name__)

# sanity check route
@common.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# accept the media user uploaded, check if the file is video, if so, save corresponding file
@common.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    response_object = {'status': 'success'}
    file = request.files['file']
    if file:
        # get file name
        filename = file.filename

        # check if the file extension is valid
        if filename.split('.')[-1] not in ['mp4', 'mp3']:
            response_object['msg'] = 'Invalid file extension'
            response_object['status'] = 'fail'
            return jsonify(response_object), 400

        # save file
        filePath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filePath)

        # file type 
        isVideo = False
        if filename.endswith('.mp4'):
            isVideo = True

        # check if the file is video, if so, capture audio
        if isVideo:
            # extract audio from video
            # TODO: not file more than 25MB due to the limit of OpenAI API
            audio = extract_audio(filePath)
            response_object['path'] = audio
        else:
            response_object['path'] = filePath

        response_object['msg'] = 'File uploaded successfully'
    else:
        response_object['msg'] = 'No file uploaded'
        response_object['status'] = 'fail'

    return jsonify(response_object)

@common.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)