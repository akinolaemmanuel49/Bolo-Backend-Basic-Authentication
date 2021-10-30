from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


class User(db.Model):

    """User object model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(230), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(102), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime)

    def __init__(self, username, pwd):
        self.username = username
        self.pwd_hash = generate_password_hash(pwd)
        self.created_on = datetime.utcnow()
        self.last_seen = datetime.utcnow()

    def generate_pwd_hash(self, plaintext_pwd):
        self.pwd_hash = generate_password_hash(plaintext_pwd)

    def check_pwd_hash(self, plaintext_pwd):
        return check_password_hash(self.pwd_hash, plaintext_pwd)

    @staticmethod
    def get(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create(username, pwd):
        user = User(username=username, pwd=pwd)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            raise SQLAlchemyError

    @staticmethod
    def update_last_seen(user):
        user.last_seen = datetime.now()
    



class Broadcast(db.Model):

    """Broadcast object model."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, message, user):
        self.message = message
        self.user_id = User.query.filter_by(id=user.id).first().id

    def get_author(self):
        return User.query.filter_by(id=self.user_id).first().username

    @staticmethod
    def post(message, user):
        broadcast = Broadcast(message=message)
        broadcast.user_id = user.id

    def __str__(self):
        return self.message
