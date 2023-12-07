import os
import datetime

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db

from blueprints.common import common
from blueprints.user import user
from blueprints.transcript import transcript

from configs import UPLOAD_FOLDER, SECRET_KEY, STATIC_FOLDER
print("upload folder path: ", UPLOAD_FOLDER)

# check if the folder exists, if not, create one
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# instantiate the app, host the static files
app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

# jwt manager
jwt = JWTManager()
# set jwt extend time to 30min
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@172.19.228.4/chatroom'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# add jwt manager to app
jwt.init_app(app)

# connect db and create all the tables if not exist
# db.init_app(app)

# Perform actions that require the application context
# with app.app_context():
#     db.create_all()

# register blueprints
app.register_blueprint(common)
app.register_blueprint(user)
app.register_blueprint(transcript)

if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
