import hashlib, string, random
from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
from app.models import Contest, Student, Submission
from app import db, utils, application, mail
from flask_mail import Message

index_bp = Blueprint("index", __name__, url_prefix='/')
SALT = "abmc_password_salt"
PASSWORD_LENGTH = 12
ACCESS_TOKEN_LENGTH = 12

@index_bp.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@index_bp.route('/sign_in', methods=['GET'])
def sign_in():
    return render_template("sign_in.html")

@index_bp.route('/register', methods=['GET'])
def register():
    return render_template("register.html")

@index_bp.route('/profile', methods=['GET'])
def profile():
    return render_template("profile.html")

@index_bp.route('/reset', methods=['GET'])
def reset():
    return render_template("reset.html")

@index_bp.route('/handle_reset', methods=['GET'])
def reset_password():
    req = request.form
    print(req)
    generated_password = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = PASSWORD_LENGTH))
    print(f'generated_password is {generated_password}') 
    h = hashlib.md5((generated_password + SALT).encode())
    s = Student.query.filter_by(email=req["email"]).first()
    s.populate(access_token, req["name"], req["email"], h.hexdigest(), req["grade"], req["gender"], req["school"], True)
    db.session.add(s)
    db.session.commit()

    msg = Message('ABMC Account Password', sender = 'abmathcompetition@gmail.com', recipients = ['awang23@mit.edu'])
    msg.body = f'''Goodday traveler,
    
This email contains the account information for user {req["name"]}.

Name: {req["name"]}
Email: {req["email"]}
School: {req["school"]}
Grade: {req["grade"]}
Password: {generated_password}

Please sign in on the submission platform using these credentials to submit your answers.

Best,
The ABMC Team
'''
    mail.send(msg)
    
    return redirect(url_for(".success"))
    return redirect(url_for(".password"))

@index_bp.route('/contest', methods=['GET'])
def contest():
    return render_template("contest.html")

@index_bp.route('/success', methods=['GET'])
def success():
    return render_template("success.html")

@index_bp.route('/no_account', methods=['GET'])
def no_account():
    return render_template("no_account.html")

@index_bp.route('/handle_register', methods=['POST'])
def handle_register():
    req = request.form
    print(req)
    generated_password = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = PASSWORD_LENGTH))
    print(f'generated_password is {generated_password}') 
    h = hashlib.md5((generated_password + SALT).encode())
    access_token = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = ACCESS_TOKEN_LENGTH))
    s = Student()
    s.populate(access_token, req["name"], req["email"], h.hexdigest(), req["grade"], req["gender"], req["school"], True)
    db.session.add(s)
    db.session.commit()

    msg = Message('ABMC Account Password', sender = 'abmathcompetition@gmail.com', recipients = ['awang23@mit.edu'])
    msg.body = f'''Goodday traveler,
    
This email contains the account information for user {req["name"]}.

Name: {req["name"]}
Email: {req["email"]}
School: {req["school"]}
Grade: {req["grade"]}
Password: {generated_password}

Please sign in on the submission platform using these credentials to submit your answers.

Best,
The ABMC Team
'''
    mail.send(msg)
    
    return redirect(url_for(".success"))
