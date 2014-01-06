from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.admin import Admin

from main import create_flask_app

import os

template_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'templates')
admin_template_dir = os.path.join(template_dir, 'admin')

# create the app here
db = SQLAlchemy()
flask_bcrypt = Bcrypt()

args = {'db':db,
        'bcrypt':flask_bcrypt}

app = create_flask_app(**args)
