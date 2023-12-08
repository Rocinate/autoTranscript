import moviepy.editor as mp

# helper function to extract the audio file from the video file
def extract_audio(video_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio_path = video_path.split('.')[0] + '.mp3'
    audio.write_audiofile(audio_path)
    return audio_path