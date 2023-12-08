import os
import datetime

from flask import Flask, render_template
from flask_cors import CORS
from flask_compress import Compress
from flask_jwt_extended import JWTManager
from models import db

from blueprints.common import common
from blueprints.user import user
from blueprints.transcript import transcript

from configs import UPLOAD_FOLDER, SECRET_KEY, STATIC_FOLDER, DATA_BASE, TEMPLATE_FOLDER
print("upload folder path: ", UPLOAD_FOLDER)

# check if the folder exists, if not, create one
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# instantiate the app, host the static files
app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

# jwt manager
jwt = JWTManager()
# set jwt extend time to 30min
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = DATA_BASE

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# add jwt manager to app
jwt.init_app(app)

# connect db and create all the tables if not exist
db.init_app(app)

# compress the response
Compress(app)

# create all the tables if not exist
with app.app_context():
    db.create_all()

# serve the react app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

# register blueprints
app.register_blueprint(common, url_prefix='/api/common')
app.register_blueprint(user, url_prefix='/api/user')
app.register_blueprint(transcript, url_prefix='/api/transcript')

if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
