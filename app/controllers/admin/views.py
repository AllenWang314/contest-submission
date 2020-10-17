from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
from app.models import Contest, Student, Submission
from app import db, mail, utils, application, utils
from flask_mail import Message

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET'])
@utils.requires_auth
def index():
    contests = Contest.query.order_by('id').all() 
    students = Student.query.order_by('id').all()
    submissions = Submission.query.order_by('id').all()

    return render_template('admin.html', 
                            contests={contest.id: contest for contest in contests}, 
                            students={student.id: student for student in students}, 
                            submissions={submission.id: submission for submission in submissions})

@admin_bp.route('/edit_student/<id>', methods=['POST'])
@utils.requires_auth
def edit_student(id):
    json_data = request.json
    s = Student.query.filter_by(id=id).first()
    s.token = json_data["token"]
    s.name = json_data["name"]
    s.email = json_data["email"]
    s.grade = json_data["grade"]
    s.gender = json_data["gender"]
    s.school = json_data["school"]
    s.active = json_data["active"]
    db.session.commit()
    return s.serialize()

@admin_bp.route('/edit_contest/<id>', methods=['POST'])
@utils.requires_auth
def edit_contest(id):
    json_data = request.json
    c = Contest.query.filter_by(id=id).first()
    c.name = json_data["name"]
    c.body = json_data["body"]
    c.num_questions = json_data["num_questions"]
    c.answers = json_data["answers"]
    c.active = json_data["active"]
    db.session.commit()
    return c.serialize()

@admin_bp.route('/post_contest', methods=['POST'])
@utils.requires_auth
def post_contest():
    json_data = request.json
    c = Contest()
    c.name = json_data["name"]
    c.body = json_data["body"]
    c.num_questions = json_data["num_questions"]
    c.answers = json_data["answers"]
    c.active = json_data["active"]
    db.session.add(c)
    db.session.commit()
    return c.serialize()

@admin_bp.route('/edit_submission/<id>', methods=['POST'])
@utils.requires_auth
def edit_submission(id):
    json_data = request.json
    s = Submission.query.filter_by(id=id).first()
    s.answers = json_data["answers"]
    db.session.commit()
    return s.serialize()

@admin_bp.route('/test_email')
@utils.requires_auth
def test_email():
    msg = Message('Test From ABMC', sender = 'abmathcompetition@gmail.com', recipients = ['awang23@mit.edu'])
    msg.body = 'Hello this is a test from the ABMC contest submission platform'
    mail.send(msg)
    return redirect(url_for('admin.index'))