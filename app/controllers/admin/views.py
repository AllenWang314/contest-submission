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

@admin_bp.route('/test_email')
@utils.requires_auth
def test_email():
    msg = Message('Test From ABMC', sender = 'abmathcompetition@gmail.com', recipients = ['awang23@mit.edu'])
    msg.body = 'Hello this is a test from the ABMC contest submission platform'
    mail.send(msg)
    return redirect(url_for('admin.index'))