import os
from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
import asyncio
from configs import UPLOAD_FOLDER
from utils import extract_audio

common = Blueprint("common", __name__)

TRANSCRIPTS = [
    {
        'title': "demo1",
        'content': "In the past week, I've made substantial headway on our software engineering project. I successfully implemented the new feature we discussed last week and rigorously tested it to ensure functionality and stability. While we encountered some challenges during integration with the existing codebase, I collaborated closely with the team to resolve these issues by refactoring parts of our code. This has not only improved the overall reliability of our application but also enhanced its performance. I've been actively engaged in our daily stand-up meetings and code review sessions, finding them incredibly valuable for aligning with the team and gaining insights from more experienced colleagues. Their feedback has been instrumental in refining my coding skills and adopting best practices. I've maintained diligent version control, meticulously documenting and committing all changes to our repository, ensuring smooth collaboration and traceability. Additionally, I've taken the initiative to research a new framework that holds promise for our future projects, keeping us updated on evolving technologies in our field. In the upcoming week, my focus will be on further refining the new feature, addressing any remaining issues, optimizing code for enhanced performance, improving the user interface, and conducting thorough testing to guarantee a seamless user experience.",
        'analysis': "In the past week, substantial progress was made on a software engineering project, including successful feature implementation, code integration, team collaboration, version control, and technology research for future improvements.",
        'task': "Summary extraction"
    },
    {
        'title': "demo2",
        'content': "Good morning to you all. I hope you had a productive week, and thank you for joining us for our weekly meeting today. Today, I'm excited to present our project plan for the upcoming sprint. As we move forward with our project, it's crucial that we stay aligned, communicate effectively, and keep our collective focus on our goals. Before we dive into the details of the plan, I want to take a moment to reflect on the progress we've made so far. Over the last sprint, we successfully completed several critical tasks and made significant headway towards our project objectives. This is a testament to your dedication, hard work, and commitment to excellence. Now, let's shift our attention to the upcoming sprint. Our primary focus for this sprint will be to build upon the foundation we've laid and continue moving towards our project milestones. Here are the key highlights of our project plan for the next sprint. Feature Development: We will prioritize the development of several key features that are essential for our project's success. Our development team will be working closely with our designers to ensure a seamless user experience. Testing and Quality Assurance: Quality is paramount. Our QA team will conduct thorough testing to identify and address any issues promptly. We'll maintain a strong feedback loop with the development team to ensure quick resolutions. Documentation: We will update and enhance our project documentation to ensure that everyone on the team has access to the most up-to-date information. This will be crucial as we scale up our efforts. Client Engagement: Our client engagement team will continue to keep our stakeholders informed about our progress, gather feedback, and address any concerns promptly. Building strong relationships with our clients is key to our project's success.",
        'analysis': "The sentiment of the text is generally positive. The speaker expresses satisfaction with past progress, excitement for future plans, and appreciation for the team's hard work and dedication.	",
        'task': "Sentiment analysis"
    }
]

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