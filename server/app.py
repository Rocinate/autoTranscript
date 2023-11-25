from flask import Flask
from flask_cors import CORS
from models import db

from blueprints.common import common
from blueprints.user import user
from blueprints.transcript import transcript

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# connect db
db.init_app(app)

# register blueprints
app.register_blueprint(common)
app.register_blueprint(user)
app.register_blueprint(transcript)

if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
