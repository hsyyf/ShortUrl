# encoding: utf-8
from datetime import timedelta


class BaseConfig(object):
    """ Default configuration options. """
    # SERVER_NAME = '127.0.0.1:5000'
    SECRET_KEY = '\x8ac\xaaH&,\xf0%\x9c\x0e\x96\x94<BI\x88\x9b\xc6K\x97\xa3}\xbc\x04'

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///short_url.db'

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_TYPE = 'sqlalchemy'
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
