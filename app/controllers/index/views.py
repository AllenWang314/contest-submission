from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
from app.models import Contest, Student, Submission
from app import db, utils, application

index_bp = Blueprint("index", __name__, url_prefix='/')

@index_bp.route('/', methods=['GET'])
def index():
    return "hello this is the index stuff"