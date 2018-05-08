
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import User
from app.engines import db

user_operate = Blueprint('user_operate', __name__, url_prefix='')
param_location = ('json', )


@user_operate.route('/user/list')
@login_required
def user_list():
    users = db.session.query(User).all()

    return render_template('user_list.html', users=users)


@user_operate.route('/user/delete/<int:user_id>')
def user_delete(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_operate.user_list'))


@user_operate.route('/user/change/<int:user_id>', methods=['POST', 'GET'])
def user_change(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if request.method == 'POST':

        name = request.form['name']

        email = request.form['email']
        role = request.form['role']
        age = request.form['age']
        location = request.form['location']
        if '管理' in role:
            role = 1
        else:
            role = 2
        password = request.form['password']
        if name == '' or email == '' or role == '' or password == '':
            flash(" 检查某些字段是否为空")
            return redirect(url_for('user_operate.user_change', user_id=user.id))

        user.name = name
        user.email = email
        user.role_id = int(role)
        user.password = password
        user.age = age
        user.location = location
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_operate.user_list'))
    return render_template('user_change.html', user=user)


@user_operate.route('/user/add', methods=['POST', 'GET'])
def user_add():
    if request.method == 'POST':

        name = request.form['name']

        email = request.form['email']
        role = request.form['role']
        age = request.form['age']
        location = request.form['location']
        # if '管理' in role:
        #     role = 1
        # else:
        #     role = 2
        password = request.form['password']
        if name == '' or email == '' or role == '' or password == '':
            flash(" 检查某些字段是否为空")
            return redirect(url_for('user_operate.user_change'))

        user = User()
        user.name = name
        user.email = email
        user.role_id = int(role)
        user.password = password
        user.age = age
        user.location = location
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_operate.user_list'))

    return render_template('user_add.html')
