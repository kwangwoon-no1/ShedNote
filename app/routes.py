# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
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
    if current_user.is_authenticated:
        return redirect(url_for('main.timetable'))
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

# 회원가입 페이지
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # 비밀번호 해싱 (보안을 위해 필요)
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)

        # 새로운 사용자 객체 생성 후 저장
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('회원가입이 완료되었습니다. 로그인 해주세요.', 'success')
        return redirect(url_for('main.login'))  # 로그인 페이지로 리디렉션

    return render_template('register.html', form=form)
