from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager


application = Flask(__name__)

# Secret key for csrf
SECRET_KEY = os.urandom(32)
application.config['SECRET_KEY'] = SECRET_KEY

#Database
application.config.from_pyfile('config.cfg')
db = SQLAlchemy(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.session_protection = "strong"
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    try:
        return User.query.filter_by(user_id=user_id).first()
    except:
        return None

from views import *

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run()
