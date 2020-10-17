import hashlib, string, random
from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
from app.models import Contest, Student, Submission
from app import db, utils, application, mail, jwt
from flask_mail import Message

index_bp = Blueprint("index", __name__, url_prefix='/')
SALT = "abmc_password_salt"
PASSWORD_LENGTH = 12
ACCESS_TOKEN_LENGTH = 12
contest_id = 1

@index_bp.route('/login', methods=['POST'])
def login(email):
    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)

    # Set the JWTs and the CSRF double submit protection cookies
    # in this response
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

@index_bp.route('/token/refresh', methods=['POST'])
def refresh():
    # Create the new access token
    print("hi")
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the access JWT and CSRF double submit protection cookies
    # in this response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200

@index_bp.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@index_bp.route('/register', methods=['GET'])
def register():
    return render_template("register.html")

@index_bp.route('/submitted', methods=['GET'])
def submitted():
    return render_template("submitted.html")

@index_bp.route('/reset', methods=['GET'])
def reset():
    return render_template("reset.html")

@index_bp.route('/handle_reset', methods=['POST'])
def handle_reset():
    req = request.form
    s = Student.query.filter_by(email=req["email"]).first()
    if (s == None):
        return redirect(url_for('.no_account'))
    generated_password = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = PASSWORD_LENGTH))
    h = hashlib.md5((generated_password + SALT).encode())
    s.password = h.hexdigest()
    db.session.commit()

    msg = Message('ABMC Account Password', sender = 'abmathcompetition@gmail.com', recipients = ['awang23@mit.edu'])
    msg.body = f'''Goodday traveler,
    
This email contains the account information for user {s.name}.

Name: {s.name}
Email: {s.email}
School: {s.school}
Grade: {s.grade}
Password: {generated_password}

If any of the above information is incorrect, please reply to this email. Sign in on the submission platform using these credentials to submit your answers.

Best,
The ABMC Team
'''
    mail.send(msg)
    
    return redirect(url_for(".success"))

@index_bp.route('/handle_submission', methods=['POST'])
def handle_submission():
    req = request.form
    s = Student.query.filter_by(email=req["email"]).one_or_none()
    c = Contest.query.filter_by(id=contest_id).one_or_none()
    if (not c.active):
        return redirect(url_for(".contest", status="expired"))
    if (s == None):
        return redirect(url_for(".contest", status="dne"))
    salted_password = hashlib.md5((req["password"] + SALT).encode())
    if (s.password != salted_password.hexdigest()):
        return redirect(url_for(".contest", status="incorrect"))
    if (s.email == req["email"] and s.password == salted_password.hexdigest()):
        answers = []
        for i in range(1,16):
            if (len(req[f"q{i}"]) == 0):
                answers.append(-1)
            else:
                answers.append(int(req[f"q{i}"]))
        submission = Submission.query.filter_by(student_id=s.id).filter_by(contest_id=contest_id).one_or_none()
        if (submission == None):
            submission = Submission()
        submission.populate(s.id, contest_id, answers, -1, -1)
        db.session.add(submission)
        db.session.commit()
        return redirect(url_for(".submitted"))
    else:
        return "Error, please contact us at abmathcompetition@gmail.com"

@index_bp.route('/contest/<status>', methods=['GET'])
def contest(status):
    contest = Contest.query.filter_by(id=contest_id).first()
    return render_template("contest.html", status=status, contest=contest)

@index_bp.route('/success', methods=['GET'])
def success():
    return render_template("success.html")

@index_bp.route('/no_account', methods=['GET'])
def no_account():
    return render_template("no_account.html")

@index_bp.route('/user_exists', methods=['GET'])
def user_exists():
    return render_template("user_exists.html")

@index_bp.route('/handle_register', methods=['POST'])
def handle_register():
    req = request.form
    generated_password = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = PASSWORD_LENGTH))
    h = hashlib.md5((generated_password + SALT).encode())
    access_token = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = ACCESS_TOKEN_LENGTH))
    
    res = Student.query.filter_by(email=req["email"]).one_or_none()
    if (res != None):
        return redirect(url_for(".user_exists"))

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
