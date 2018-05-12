from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.engines import db
from app.models import User, Log
from flask_login import login_required, current_user
from flask_login import login_user, logout_user, login_required
auth = Blueprint('auth', __name__, url_prefix='')
param_location = ('json', )


@auth.route('/admin/login/user', methods=['POST', 'GET'])   # 用户登录请求处理
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.session.query(User).filter_by(email=email).first()

        if user:
            if user.password == password:
                login_user(user, remember=True)
                log = Log()
                log.user = user.name
                log.operate = '帐号登录'
                db.session.add(log)
                db.session.commit()
                return redirect(url_for('ib.index'))
            else:
                flash("密码错误，再试一次")
                return render_template('login.html')
        else:
            flash("没有此用户，检查输入")
            return render_template('login.html')
    return render_template('login.html')


@auth.route('/login/user', methods=['POST', 'GET'])   # 用户登录请求处理
def front_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.session.query(User).filter_by(email=email).first()

        if user:
            if user.password == password:
                login_user(user, remember=True)
                log = Log()
                log.user = user.name
                log.operate = '帐号登录'
                db.session.add(log)
                db.session.commit()
                return redirect(url_for('front_index.index'))
            else:
                return redirect(url_for('front_index.login'))
        else:
            return redirect(url_for('front_index.login'))
    return redirect(url_for('front_index.login'))


@auth.route('/admin/logout', methods=['POST', 'GET'])    # 用户登出请求处理
@login_required
def logout():
    log = Log()
    log.user = current_user.name
    log.operate = '帐号登出'
    db.session.add(log)
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/admin/register', methods=['POST', 'GET'])     # 用户注册请求处理
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = db.session.query(User).filter_by(email=email).first()

        if user:
            flash(" 此邮箱已被注册")
            return render_template('register.html')

        if password1 != password2:
            flash("两次输入密码不一致")
            return render_template('register.html')

        user = User()
        user.name = name
        user.email = email
        user.password = password1
        user.role_id = 2
        db.session.add(user)
        db.session.commit()
        log = Log()
        log.user = name
        log.operate = '帐号注册'
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')