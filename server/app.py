from flask import Flask
from flask_cors import CORS
from models import db

# from blueprints.common import common
from blueprints.user import user
from blueprints.transcript import transcript

# instantiate the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@172.19.228.4/chatroom'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# connect db and create all the tables if not exist
db.init_app(app)
db.create_all()

# register blueprints
# app.register_blueprint(common)
app.register_blueprint(user)
app.register_blueprint(transcript)

if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
