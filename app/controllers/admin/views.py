from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
from app.models import Contest, Student, Submission
from app import db, utils, application

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET'])
def index():
    return "hello this is the admin stuff"