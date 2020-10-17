import os
from flask import Flask, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

application = None
db = None
mail = None

# sets config from environment variables
def load_from_env(app, *args):
    for a in args:
        app.config[a] = os.environ[a]

def create_app():
    global application, db, bcrypt, session, mail

    application = Flask(__name__, static_folder='static')

    # load main config
    if os.path.exists("config.py"):
        application.config.from_pyfile('../config.py')
        print("Loading secret configs from file")
    else:
        # TODO add load_from_env call
        print("Loading from environment variables")

    # set up tokens
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = True
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True

    # set up emails
    application.config['MAIL_SERVER'] ='smtp.gmail.com'
    application.config['MAIL_PORT'] = 465
    application.config['MAIL_USE_TLS'] = False
    application.config['MAIL_USE_SSL'] = True
    mail = Mail(application)

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
