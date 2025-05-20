import hashlib
import random
from flask import session

def generate_csrf_token():
    """
    Generate a CSRF token to be included in the form.
    """
    csrf_token = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()
    session['csrf_token'] = csrf_token
    return csrf_token

def validate_csrf_token(token):
    """
    Validate CSRF token from the user request with the token stored in session.
    """
    return session.get('csrf_token') == token
