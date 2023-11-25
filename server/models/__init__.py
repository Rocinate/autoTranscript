from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    registered_on = db.Column(db.DateTime, nullable = False, default = db.func.current_timestamp())
    chat_times = db.Column(db.Integer, nullable = False, default = 0)
    require_times = db.Column(db.Integer, nullable = False, default = 0)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        return f"{self.username} {self.email}"

class Transcript(db.Model):
    __tablename__ = 'transcripts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.longtext, nullable = False)
    analysis = db.Column(db.String(50), nullable = False)
    task = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    created_on = db.Column(db.DateTime, nullable = False, default = db.func.current_timestamp())
    audio_path = db.Column(db.String(50), nullable = False, default = False)

    def __init__(self, title, content, analysis, task, user_id, audio_path):
        self.title = title
        self.content = content
        self.analysis = analysis
        self.task = task
        self.user_id = user_id
        self.audio_path = audio_path

class TransHistory(db.Model):
    __tablename__ = 'transHistory'
    id = db.Column(db.Integer, primary_key = True)
    parent_id = db.Column(db.Integer, db.ForeignKey('transcripts.id'), nullable = False)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(1000), nullable = False)
    analysis = db.Column(db.String(1000), nullable = False)
    task = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    created_on = db.Column(db.DateTime, nullable = False, default = db.func.current_timestamp())
    audio_path = db.Column(db.String(50), nullable = False, default = False)

    def __init__(self, parent_id, title, content, analysis, task, user_id, audio_path):
        self.parent_id = parent_id
        self.title = title
        self.content = content
        self.analysis = analysis
        self.task = task
        self.user_id = user_id
        self.audio_path = audio_path