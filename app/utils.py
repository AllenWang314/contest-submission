from functools import wraps
from flask import Response, request
from app import application

def authenticate():
    return Response('Access denied.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def check_auth(username, password):
    return username == application.config['ADMIN_USERNAME'] and application.config['ADMIN_PASSWORD']

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
