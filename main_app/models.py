from main_app import db
from flask_login import UserMixin
from main_app import login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,unique=True)
    email = db.Column(db.String,unique=True)
    password = db.Column(db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password,password)

class Texts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_username = db.Column(db.String, nullable=False)
    to_username = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    def __init__(self, from_username, to_username, text):
        self.from_username = from_username
        self.to_username = to_username
        self.text = text