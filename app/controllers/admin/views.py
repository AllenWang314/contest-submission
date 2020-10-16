from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
from app.models import Contest, Student, Submission
from app import db, mail, utils, application
from flask_mail import Message

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET'])
def index():
    return "hello this is the admin stuff"

@admin_bp.route('/test_email')
def test_email():
    msg = Message('Test From ABMC', sender = 'abmathcompetition@gmail.com', recipients = ['awang23@mit.edu'])
    msg.body = 'Hello this is a test from the ABMC contest submission platform'
    mail.send(msg)
    return redirect(url_for('admin.index'))