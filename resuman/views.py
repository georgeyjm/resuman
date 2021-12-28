import re
import sys
import traceback
from functools import wraps

from flask import Response, request, render_template, send_file, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from flask import current_app as app

from resuman.utils import render_resume

# from resuman import db, login_manager, cache
# from .models import Student, User, Message
# from .forms import LoginForm, MessageForm
# from .helper import ykps_auth, record_change



#################### Web Pages ####################

@app.route('/')
# @cache.cached(timeout=3600)
def index_page():
    return 'Hello'


@app.route('/render/<int:resume_id>')
# @cache.cached(timeout=3600)
def render(resume_id):
    render_resume(resume_id)
    return 'Hello'
