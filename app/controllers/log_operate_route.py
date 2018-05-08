
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Log
from app.engines import db

log_operate = Blueprint('log_operate', __name__, url_prefix='')
param_location = ('json', )


@log_operate.route('/log/list')
@login_required
def log_list():
    logs = db.session.query(Log).all()

    return render_template('log_list.html', logs=logs)




