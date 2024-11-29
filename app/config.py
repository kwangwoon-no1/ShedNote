# app/config.py
class Config:
    SECRET_KEY = 'your-secret-key-here'  # CSRF와 세션을 위한 비밀 키
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/shednote.db'  # SQLite DB URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # SQLAlchemy의 변경 추적 비활성화
