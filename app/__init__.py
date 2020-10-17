import os
from flask import Flask, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import JWTManager

application = None
db = None
mail = None
jwt = None

# sets config from environment variables
def load_from_env(app, *args):
    for a in args:
        app.config[a] = os.environ[a]

def create_app():
    global application, db, bcrypt, session, mail, jwt

    application = Flask(__name__, static_folder='static')

    # load main config
    if os.path.exists("config.py"):
        application.config.from_pyfile('../config.py')
        print("Loading secret configs from file")
    else:
        load_from_env(application, 'SQLALCHEMY_DATABASE_URI',
                                    'DEBUG',
                                    'SQLALCHEMY_TRACK_MODIFICATIONS',
                                    'DEPLOY',
                                    'ADMIN_USERNAME',
                                    'ADMIN_PASSWORD',
                                    'MAIL_DEBUG',
                                    'MAIL_USERNAME',
                                    'MAIL_PASSWORD',
                                    'JWT_SECRET_KEY')

    # set up tokens
    application.config['JWT_TOKEN_LOCATION'] = ['cookies']
    application.config['JWT_COOKIE_SECURE'] = False
    application.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
    application.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
    application.config['JWT_COOKIE_CSRF_PROTECT'] = True
    jwt = JWTManager(application)

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
