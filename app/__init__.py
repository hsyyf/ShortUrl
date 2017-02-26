# encoding: utf-8
import os

from flask import redirect
from flask import render_template
from flask import send_from_directory

from app import appconfig

from app.extension import app, login_manager, bcrypt, session
from app.model import User
from app.util.mysql_util import db

from app import views


def create_app(config=appconfig.BaseConfig):
    app.config.from_object(config)
    register_extension(app)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static/img'),
                                   'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    @app.route('/robot.txt')
    def robot():
        return send_from_directory(os.path.join(app.root_path, 'static/'),
                                   'robot.txt',
                                   mimetype='text/plain')

    @app.errorhandler(404)
    def not_fund(error):
        return render_template('404.html')

    return app


def register_extension(app_conf):
    init_login_manager(app_conf)
    db.init_app(app_conf)
    bcrypt.init_app(app_conf)
    session.init_app(app_conf)


def init_login_manager(app_conf):
    login_manager.init_app(app_conf)
    login_manager.session_protection = 'strong'
    login_manager.login_view = '/'


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(login_manager.login_view)
