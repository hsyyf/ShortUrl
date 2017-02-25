# encoding : utf-8
from app import create_app
from app.util.mysql_util import db
from app.appconfig import BaseConfig

db.create_all(app=create_app(BaseConfig))
