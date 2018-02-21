from db import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = "user"

    userid = db.Column('userid', db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, full_name, email, password):
        self.full_name = full_name
        self.email = email
        self.set_password(password)
        self.username = ""

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if password:
            return check_password_hash(self.password, password)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            return {"message", e}

    def json(self):
        return {'id': self.userid, 'full_name': self.full_name, 'email': self.email, 'username': self.username}
