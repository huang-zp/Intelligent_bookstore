from flask import Blueprint, render_template, request, flash, redirect, url_for

from datetime import datetime, timedelta
from app.models import User
from app.engines import db
from flask_login import login_required, current_user


info = Blueprint('info', __name__, url_prefix='')
param_location = ('json', )


@info.route('/info', methods=['POST', 'GET'])
@login_required
def user_info():
    if request.method == 'POST':

        user = db.session.query(User).filter(User.id == current_user.id).first()
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        location = request.form['location']
        if name == '' or email == '':
            flash('字段不能空')
            redirect(url_for('info.user_info'))
        user.name = name
        user.email = email
        user.age = age
        user.location = location
        db.session.add(user)
        db.session.commit()
        flash('修改成功')

    return render_template('user_info.html')