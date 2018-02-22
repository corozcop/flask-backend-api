from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, exc
import random
from datetime import datetime
import uuid
import logging.config

logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

ausergroup = db.Table('users_groups',
  db.Column('id', db.Integer, primary_key=True),
  db.Column('user_id', db.Integer, db.ForeignKey('user.userid', onupdate="CASCADE", ondelete="RESTRICT")),
  db.Column('group_id', db.Integer, db.ForeignKey('group.groupid', onupdate="CASCADE", ondelete="RESTRICT"))
  )


class UserModel(db.Model):
    __tablename__ = "user"

    userid = db.Column('userid', db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    uuid = db.Column(db.String(255))
    ugroups = db.relationship('GroupModel', secondary=ausergroup, backref=db.backref('group', lazy='dynamic'))

    def __init__(self, full_name, email, password):
        self.full_name = full_name
        self.email = email
        self.set_password(password)
        self.username_generator()
        self.created_at = datetime.utcnow()
        self.uuid = str(uuid.uuid4())

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter(func.lower(cls.email) == func.lower(email)).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter(func.lower(cls.username) == func.lower(username)).first()

    @classmethod
    def valid_user(cls, password):
        return check_password_hash(cls.password, password)

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
            log.error(str(e))
            return {"message", "something went wrong"}

    def json(self):
        return {
            'id': self.userid,
            'full_name': self.full_name,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'groups': [g.json() for g in self.ugroups]
        }

    def username_generator(self):
        fullname = self.full_name.lower().split()
        if len(fullname) > 1:
            first_letter = fullname[0][0]
            three_letters_surname = fullname[-1][:3].rjust(3, 'x')
            number = '{:03d}'.format(random.randrange(1, 999))
            self.username = '{}{}{}'.format(first_letter, three_letters_surname, number)
        else:
            surname = self.email.split('@')
            self.username = surname[0]+str(random.randrange(1, 999))


class GroupModel(db.Model):
    __tablename__ = 'group'
    groupid = db.Column('groupid', db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(100))

    def __init__(self, name, description):
        self.name = name.capitalize()
        self.description = description

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(groupid=_id).first()

    @classmethod
    def find_by_name(cls, _name):
        return cls.query.filter(func.lower(cls.name) == func.lower(_name)).first()

    def json(self):
        return {'groupid': self.groupid, 'name': self.name, 'description': self.description}

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.error(str(e))
            return {"message": "something went wrong"}

