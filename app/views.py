# encoding: utf-8

from flask import redirect
from flask import render_template, request
from flask_login import current_user, login_required, login_user, logout_user

from app import app
from app.util.Response_util import SuccResponse, ErrResponse
from app.util.map_util import change_into_short, match_url, in_black, format_url
from app.model import User, ShortUrl, Constant, BlackList


@app.route('/install', methods=['GET', 'POST'])
def install():
    user = User.query.filter_by().first()
    if user:
        return redirect('/')

    if request.method == 'GET':
        return render_template('install.html')

    req_data = request.json
    name = req_data.get('name', None)
    password = req_data.get('password', None)
    confirm_password = req_data.get('confirm_password', None)
    domain = req_data.get('domain', None)

    if not all([name, password, confirm_password, domain]):
        ErrResponse()
    if password != confirm_password:
        ErrResponse()
    User.create(name=name, password=password)
    Constant.create(kind='constant', code='main_url', name=domain, value=domain)
    return SuccResponse()


@app.route('/', methods=['GET'])
def index():
    user = User.query.filter_by().first()
    if not user:
        return render_template('install.html')
    return render_template('index.html')


@app.route('/index', methods=['GET'])
def index_copy():
    user = User.query.filter_by().first()
    if not user:
        render_template('install.html')
    return render_template('index.html')


@app.route('/change', methods=['POST'])
def change():
    req_data = request.json
    long_url = req_data.get('url')
    if not long_url:
        return ErrResponse()

    domain = format_url(url=long_url)
    if BlackList.query.filter_by(black=domain).first():
        return ErrResponse()
    long_url = match_url(long_url)

    main_url = Constant.query.filter_by(code='main_url').first()
    if not main_url:
        domain = ''
    else:
        domain = main_url.name
    if in_black(long_url):
        return ErrResponse()
    hash_key = change_into_short(long_url)
    short_url = domain + r'/s/' + hash_key

    url = ShortUrl.query.filter_by(short_url=short_url).first()
    if not url:
        ShortUrl.create(
            short_url=short_url,
            long_url=long_url,
            hash_key=hash_key
        )

    return SuccResponse({'url': short_url})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    req_data = request.json
    name = req_data.get('name', None)
    password = req_data.get('password', None)
    user = User.query.filter_by(name=name).first()
    if not user:
        return ErrResponse()
    if user.check_password(password):
        login_user(user)
        return SuccResponse()
    else:
        return ErrResponse()


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return SuccResponse()


@app.route('/login_status', methods=['GET'])
def login_status():
    if hasattr(current_user, 'id'):
        return SuccResponse()
    else:
        return ErrResponse()


@app.route('/s/<url>', methods=['GET'])
def redirecting(url):
    if not url:
        return redirect('/')

    main_url = Constant.query.filter_by(code='main_url').first()
    if not main_url:
        domain = 't.cn'
    else:
        domain = main_url.name
    short_url = domain + '/s/' + url
    url_total = ShortUrl.query.filter_by(short_url=short_url).first()

    if not url_total:
        return redirect('/')

    return redirect(url_total.long_url)


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    return render_template('admin.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return SuccResponse({'name': User.get_by_id(current_user.id).name})

    req_data = request.json

    name = req_data.get('name', None)

    old_password = req_data.get('old_password', None)
    password = req_data.get('password', None)
    confirm_password = req_data.get('confirm_password', None)

    if not name:
        return ErrResponse()

    user = User.get_by_id(current_user.id)
    print(name, old_password, password, confirm_password)
    if not any([old_password, password, confirm_password]):
        user.name = name
        user.update()
    elif all([old_password, password, confirm_password]):
        if not user.check_password(old_password):
            return ErrResponse()

        if password != confirm_password:
            return ErrResponse()
        user.name = name
        user.set_password(password)
        user.update()
        return SuccResponse()
    else:
        return ErrResponse()
    return SuccResponse()


@app.route('/black_list', methods=['GET'])
@login_required
def black_list():
    if request.method == 'GET':
        url_list = BlackList.query.filter_by().all()
        res = [i.black for i in url_list]
        return SuccResponse({'url_list': res})


@app.route('/add_url', methods=['POST'])
@login_required
def add_url():
    url = request.json.get('url', None)
    if not url:
        return ErrResponse()
    domain = format_url(url)
    if not BlackList.query.filter_by(black=domain).first():
        BlackList.create(black=domain)
        return SuccResponse()
    return ErrResponse()


@app.route('/del_url', methods=['POST'])
def del_url():
    url = request.json.get('url', None)
    if not url:
        return ErrResponse()

    for i in url:
        domain = BlackList.query.filter_by(black=i).first()
        if not domain:
            pass
        else:
            domain.delete()
    return SuccResponse()
