# encoding: utf-8
from flask_login import UserMixin

from app.extension import bcrypt

from app.util.mysql_util import db, CRUDMixin


class Constant(CRUDMixin, db.Model):
    kind = db.Column(db.String(512), nullable=False)
    code = db.Column(db.String(1024), nullable=False)
    name = db.Column(db.String(32))
    value = db.Column(db.String(32))

    def __init__(self, kind, code, name, value):
        self.kind = kind
        self.code = code
        self.name = name
        self.value = value


class ShortUrl(CRUDMixin, db.Model):
    short_url = db.Column(db.String(32))
    long_url = db.Column(db.String(512))
    hash_key = db.Column(db.String(32))

    def __init__(self, short_url, long_url, hash_key):
        self.short_url = short_url
        self.long_url = long_url
        self.hash_key = hash_key

    @property
    def json(self):
        return {'short_url': self.short_url,
                'long_url': self.long_url}


class User(UserMixin, CRUDMixin, db.Model):
    name = db.Column(db.String(32))
    password = db.Column(db.String(128))
    is_active = db.Column(db.BOOLEAN)

    def __init__(self, name, password):
        self.name = name
        self.set_password(password)
        self.is_active = True

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def get_by_name(cls, name):
        user = cls.query.filter_by(name=name).first()
        return user


class BlackList(CRUDMixin, db.Model):
    black = db.Column(db.String(64))

    def __init__(self, black):
        self.black = black
