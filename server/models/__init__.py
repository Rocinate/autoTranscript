from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    registered_on = db.Column(db.DateTime, nullable = False, default = db.func.current_timestamp())
    require_times = db.Column(db.Integer, nullable = False, default = 0)
    transcription_count = db.Column(db.Integer, nullable = False, default = 0)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        return f"{self.username} {self.email}"
    
    def check_password(self, password):
        if password == self.password:
            return True
        return False

class Transcript(db.Model):
    __tablename__ = 'transcripts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text, nullable = False)
    task = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    created_on = db.Column(db.DateTime, nullable = False, default = db.func.current_timestamp())
    status = db.Column(db.String(10), nullable = False, default = 'Running')
    analysis = db.Column(db.Text, nullable = True)
    audio_name = db.Column(db.String(200), nullable = True)

    def __init__(self, title, content,task, user_id, status = "Running", analysis = None, audio_name = None):
        self.title = title
        self.content = content
        self.analysis = analysis
        self.task = task
        self.user_id = user_id
        self.status = status
        self.audio_name = audio_name

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "task": self.task,
            "created_on": self.created_on,
            "status": self.status,
            "analysis": self.analysis,
            "audio_path": f"/common/file/{self.audio_name}" if self.audio_name else ""
        }

class TransHistory(db.Model):
    __tablename__ = 'transHistory'
    id = db.Column(db.Integer, primary_key = True)
    parent_id = db.Column(db.Integer, db.ForeignKey('transcripts.id'), nullable = False)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text, nullable = False)
    analysis = db.Column(db.Text, nullable = False)
    task = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    created_on = db.Column(db.DateTime, nullable = False, default = db.func.current_timestamp())
    status = db.Column(db.Boolean, nullable = False, default = True)
    audio_name = db.Column(db.String(200), nullable = True)

    def __init__(self, parent_id, title, content, analysis, task, user_id, status = "Running", audio_name = None):
        self.parent_id = parent_id
        self.title = title
        self.content = content
        self.analysis = analysis
        self.task = task
        self.user_id = user_id
        self.status = status
        self.audio_name = audio_name