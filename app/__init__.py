import os
from flask import Flask, session, request
from flask_sqlalchemy import SQLAlchemy

application = None
db = None
mail = None

# sets config from environment variables
def load_from_env(app, *args):
    for a in args:
        app.config[a] = os.environ[a]

def create_app():
    global application, db

    application = Flask(__name__, static_folder='static')

    # load main config
    if os.path.exists("config.py"):
        application.config.from_pyfile('../config.py')
        print("Loading secret configs from file")
    else:
        print("Loading from environment variables")

    # load database
    db = SQLAlchemy(application)
    from app.models import Contest, Student, Submission

    # register module blueprints
    from app.controllers.admin.views import admin_bp
    from app.controllers.index.views import index_bp
    application.register_blueprint(admin_bp)
    application.register_blueprint(index_bp)

    db.create_all()

    return application
