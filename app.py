import datetime
import logging
# noinspection PyUnresolvedReferences
from logging import debug, info, warning, error, critical

from flask import Flask, redirect, render_template
# noinspection PyUnresolvedReferences
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from forms import LoginForm, SignupForm, FreeForm

import sqlite3
from db import sql_gate

props = {
    'app_name': '777cold-snap',
    'db_path': 'db/db.db',
    'titles': {'/': '777cold-snap',
               '/login': 'Вход',
               '/signup': 'Регистрация',
               '/pay': 'Пополнение',
               '/free': 'Халява'}
}

logging.basicConfig(
    filename='log.log',
    format='[$asctime] [$levelname] [$name]\t>>> $message',
    datefmt='%Y-%m-%d %H:%M:%S',
    style='$',
    level=logging.DEBUG,
    encoding='utf-8',
    force=True)

info('starting app' + ('\n' + '-' * 100 + '\n') * 3)

con = sqlite3.connect(props['db_path'], check_same_thread=False)

app = Flask(props['app_name'])
app.config['SECRET_KEY'] = 'the_password_is_eight_asterisks'  # todo возможно надо рандомить, но я не уверен
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)


class AppError(Exception):
    pass


class User:
    is_active = True
    is_anonymous = False

    def __init__(self, user_id):

        data = sql_gate.get_users(con, user_id=user_id)

        if len(data) == 0:
            self.is_authenticated = False
            raise AppError('ЭТА ВЕТКА ВООБЩЕ ВОЗМОЖНА? Если это  important')
        else:
            data = data[0]
            if not isinstance(data, tuple):
                err = f'user object must receive a tuple not {type(data)} with data {repr(data)}'
                error(err)
                raise AppError('ТЫ ДАУН???')
            self.is_authenticated = True
            self.id, self.password, self.email, self.money = data

    def get_id(self):
        return self.id

    def __str__(self):
        return f'email: {self.email} auth: {self.is_authenticated}'


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def reload_current_user():
    user = load_user(current_user.id)
    login_user(user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = sql_gate.get_users(con, email=form.data['email'],
                                  password=form.data['password'])
        if user:
            login_user(User(user[0][0]), remember=True)
            info(f'user {current_user.id} logged in')
            return redirect('/')
    return render_template('login.html',
                           props=props,
                           form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        data = sql_gate.get_users(con, email=form.data['email'])
        if len(data) != 0:
            form.email.errors.append('почта уже занята!')
        else:
            sql_gate.add_user(con, form.data['email'], form.data['password1'])
            return redirect('/login')
    return render_template('signup.html',
                           props=props,
                           form=form)


@app.route('/')
def index():
    return render_template('index.html',
                           props=props)


@app.route('/pay')
def pay():
    return render_template('pay.html',
                           props=props)


@login_required
@app.route('/free', methods=['GET', 'POST'])
def free():
    form = FreeForm()
    if form.validate_on_submit():
        sql_gate.add_money(con, current_user.id, form.data['money'])
        info(f'free money gained: user: {current_user.id}, money: {form.data["money"]}')
        reload_current_user()
    return render_template('free.html',
                           props=props,
                           form=form)
