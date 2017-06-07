# encoding: utf-8
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
bcrypt = Bcrypt()
login_manager = LoginManager()
