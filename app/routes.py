# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm

main = Blueprint('main', __name__)

# 홈 페이지
@main.route('/')
def home():
    return redirect(url_for('main.login'))

# 로그인 페이지
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('main.timetable'))  # 로그인 후 timetable로 리디렉션
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

# 로그아웃
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

# 시간표 페이지
@main.route('/timetable')
@login_required
def timetable():
    return render_template('timetable.html')

# 저장소 페이지 (새로 추가)
@main.route('/storage')
@login_required
def storage():
    return render_template('storage.html')
