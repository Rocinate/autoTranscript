from openai import OpenAI
from models import User, Transcript, TransHistory, db

# client = OpenAI()

async def create_task(transcript):
    # if audio file is provided, convert it to text
    if transcript.audio_path:
        text = audio2text(transcript.audio_path)
        transcript.content = text

    # run the task
    run_test(transcript)

    # update the transcript status
    transcript.finished = True

    # save the transcript update
    db.session.commit()

    return True

def audio2text(audio_path):
    pass


def run_test():
    pass

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