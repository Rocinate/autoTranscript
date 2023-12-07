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
        file.save(UPLOAD_FOLDER, filename)
        filePath = os.path.join(UPLOAD_FOLDER, filename)

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

# @app.route('/transcripts', methods=['GET', 'POST'])
# def all_transcripts():
#     response_object = {'status': 'success'}
#     if request.method == 'POST':
#         post_data = request.get_json()
#         print(post_data)
#         task = post_data.get('task')
#         content = post_data.get('content')

#         if task == "Key points identification":
#             analysis = key_points_extraction(content)
#         if task == "Summary extraction":
#             analysis = summary_extraction(content)
#         if task == "Action item extraction":
#             analysis = key_points_extraction(content)
#         if task == "Sentiment analysis":
#             analysis = sentiment_analysis(content)
        
#         TRANSCRIPTS.append({
#             'title': post_data.get('title'),
#             'content': post_data.get('content'),
#             'analysis': analysis,
#             'task': task
#         })
#         response_object['message'] = "Your transcript's analysis has been generated!"
#     else:
#         response_object['transcripts'] = TRANSCRIPTS
#     return jsonify(response_object)


# def summary_extraction(transcript):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points. Please use less than 30 words."
#             },
#             {
#                 "role": "user",
#                 "content": transcript
#             }
#         ]
#     )
#     return response.choices[0].message.content

# def key_points_extraction(transcript):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about. Please use less than 30 words."
#             },
#             {
#                 "role": "user",
#                 "content": transcript
#             }
#         ]
#     )
#     return response.choices[0].message.content


# def action_item_extraction(transcript):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely. Please use less than 30 words."
#             },
#             {
#                 "role": "user",
#                 "content": transcript
#             }
#         ]
#     )
#     return response.choices[0].message.content

# def sentiment_analysis(transcript):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible. Please use less than 30 words."
#             },
#             {
#                 "role": "user",
#                 "content": transcript
#             }
#         ]
#     )
#     return response.choices[0].message.content