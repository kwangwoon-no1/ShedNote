from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # 로그인 페이지로 리디렉션

    from app.models import User

    # user_loader 함수 등록
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # 사용자 ID로 User 객체 로드

    # 블루프린트 등록
    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app



