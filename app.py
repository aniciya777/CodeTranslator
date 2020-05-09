from pprint import pprint

from flask import Flask, render_template, request, redirect, send_from_directory, current_app, \
    url_for

from config import *
from functions import detect_lang, translate, replacer
from hashlib import md5
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email as EmailValidator, EqualTo, \
    Length as LengthValidator, Regexp as RegexpValidator
from flask_wtf.file import FileAllowed
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_avatars import Avatars
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/database.sqlite")
session = db_session.create_session()
avatars = Avatars(app)
app.config['AVATARS_SAVE_PATH'] = AVATARS_SAVE_PATH
logging.basicConfig(level=logging.ERROR)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


class Stripped(object):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].strip()
        else:
            self.data = ''


class StrippedStringField(Stripped, StringField):
    pass


class StrippedPasswordField(Stripped, PasswordField):
    pass


class LoginForm(FlaskForm):
    email = StrippedStringField('Почта', validators=[
        DataRequired(message='Введите почту'),
        EmailValidator(message='Неверный адрес электронной почты')
    ])
    password = StrippedPasswordField('Пароль', validators=[
        DataRequired(message='Введите пароль')
    ])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StrippedStringField('Почта', validators=[
        DataRequired(message='Введите почту'),
        EmailValidator()
    ])
    password = StrippedPasswordField('Пароль', validators=[
        DataRequired(message='Введите пароль'),
        LengthValidator(min=MIN_PASSWORD_LENGTH, message=f'Длина пароля более {MIN_PASSWORD_LENGTH} символов'),
        RegexpValidator(r'(?=.*[a-zA-Z])(?=.*[0-9])', flags=0, message='Пароль должен содержать цифры и буквы латинского алфавита')
    ])
    password_2 = StrippedPasswordField('Повторите пароль', validators=[
        DataRequired(message='Введите пароль ещё раз'),
        EqualTo('password', 'Пароли не совпадают')
    ])
    photo = FileField('Фото профиля', validators=[
        FileAllowed(['jpg', 'png'], 'The file format should be .jpg or .png.')
    ])
    submit = SubmitField('Зарегистрироваться')


class PhotoUpdateForm(FlaskForm):
    photo = FileField('Фото профиля', validators=[
        FileAllowed(['jpg', 'png'], 'The file format should be .jpg or .png.'),
        DataRequired(message='Загрузите новое фото'),
    ])
    submit = SubmitField('Загрузить')


class PasswordUpdateForm(FlaskForm):
    password_old = StrippedPasswordField('Старый пароль', validators=[
        DataRequired(message='Введите старый пароль')
    ])
    password = StrippedPasswordField('Новый пароль', validators=[
        DataRequired(message='Введите новый пароль'),
        LengthValidator(min=MIN_PASSWORD_LENGTH, message=f'Длина пароля более {MIN_PASSWORD_LENGTH} символов'),
        RegexpValidator(r'(?=.*[a-zA-Z])(?=.*[0-9])', flags=0, message='Пароль должен содержать цифры и буквы латинского алфавита')
    ])
    password_2 = StrippedPasswordField('Повторите новый пароль', validators=[
        DataRequired(message='Введите новый пароль ещё раз'),
        EqualTo('password', 'Пароли не совпадают')
    ])
    submit = SubmitField('Сменить пароль')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password.data.strip()
        user = session.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password.data.strip()
        user = session.query(User).filter(User.email == email).first()
        if user:
            return render_template('register.html',
                                   message="Пользователь с такой почтой уже зарегистрирован",
                                   form=form)
        new_user = User(email=email)
        new_user.set_password(password)
        if request.files:
            f = request.files.get('photo')
            if f:
                raw_filename = avatars.save_avatar(f)
                new_user.avatar_s = url_for('get_avatar', filename=raw_filename)
                new_user.avatar_m = url_for('get_avatar', filename=raw_filename)
                new_user.avatar_l = url_for('get_avatar', filename=raw_filename)
        session.add(new_user)
        session.commit()
        login_user(new_user, remember=True)
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile')
@login_required
def profile():
    photo_update_form = PhotoUpdateForm()
    password_update_form = PasswordUpdateForm()
    return render_template('profile.html', not_show_avatar=True,
                           photo_update_form=photo_update_form,
                           password_update_form=password_update_form)


def delete_photos(user_id):
    user = session.query(User).get(user_id)
    if user.avatar_s:
        try:
            os.remove(f'static/img{user.avatar_s}')
        except BaseException as e:
            logging.error(f'Error delete avatar_s for user {user} - {e}')
        finally:
            user.avatar_s = None
    if user.avatar_m:
        try:
            os.remove(f'static/img{user.avatar_m}')
        except BaseException as e:
            logging.error(f'Error delete avatar_m for user {user} - {e}')
        finally:
            user.avatar_m = None
    if user.avatar_l:
        try:
            os.remove(f'static/img{user.avatar_l}')
        except BaseException as e:
            logging.error(f'Error delete avatar_l for user {user} - {e}')
        finally:
            user.avatar_l = None
    session.commit()


@app.route('/remove_account', methods=['POST'])
@login_required
def remove_account():
    user_id = current_user.id
    delete_photos(user_id)
    logout_user()
    user = session.query(User).get(user_id)
    session.delete(user)
    return render_template('account_removed.html')


@app.route('/update_photo', methods=['POST'])
@login_required
def update_photo():
    form = PhotoUpdateForm()
    if form.validate_on_submit():
        delete_photos(current_user.id)
        user = session.query(User).get(current_user.id)
        if request.files:
            f = request.files.get('photo')
            if f:
                raw_filename = avatars.save_avatar(f)
                user.avatar_s = url_for('get_avatar', filename=raw_filename)
                user.avatar_m = url_for('get_avatar', filename=raw_filename)
                user.avatar_l = url_for('get_avatar', filename=raw_filename)
        session.commit()
    return redirect('/profile')


@app.route('/update_password', methods=['POST'])
@login_required
def update_password():
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        user = session.query(User).get(current_user.id)
        password_old = form.password_old.data.strip()
        if not user.check_password(password_old):
            return render_template('error_update_password.html', error='Введён неправильный старый пароль.')
        password = form.password.data.strip()
        if password_old == password:
            return render_template('error_update_password.html', error='Старый и новый пароли совпадают.')
        user.set_password(password)
        session.commit()
        logout_user()
        return redirect('/login')
    return redirect('/profile')


@app.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.form.get('hidden_download', 'false') == 'true':
        return download()
    inputText = request.form.get('inputText', '').strip()
    file_name = None
    try:
        if request.files:
            file_name = request.files['files'].filename
            f = request.files['files'].read()
            if f:
                inputText = f.decode('utf-8')
    except BaseException:
        pass
    lang1_key = request.form.get('inputGroupSelectLanguageFrom', '')
    lang2_key = request.form.get('inputGroupSelectLanguageTo', '')
    selectType = request.form.get('selectType', 'text')
    outputText = ''
    parser = PARSERS[selectType]
    if inputText:
        data = parser['parser'](inputText)
        if not lang1_key or lang1_key == 'auto':
            lang1_key = detect_lang(data)
        data = translate(data, lang1_key, lang2_key)
        outputText = replacer(inputText, data)
    LANGS_TO = {key: val for key, val in LANGS.items() if key in DIRS.get(lang1_key, set())}
    params = {
        'PARSERS': PARSERS,
        'LANGS_FROM': LANGS_FROM,
        'LANGS_TO': LANGS_TO,
        'lang1_key': lang1_key,
        'lang2_key': lang2_key,
        'inputText': inputText,
        'outputText': outputText,
        'selectType': selectType,
        'dir_json': DIR_JSON,
        'langs_json': LANGS_JSON,
        'file_name': file_name,
    }
    if not params['file_name']:
        params['file_name'] = 'translate.' + parser['files'][0]
    return render_template('index.html', **params)


def download():
    text = request.form.get('outputText', '')
    temp_path = DOWNLOAD_FILE_PATH + str(md5(text.encode('utf-8')).hexdigest())
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(text)
    filename = request.form.get('hidden_file_name', 'translate.txt')

    def generate():
        with open(temp_path) as f:
            yield from f
        os.remove(temp_path)

    r = app.response_class(generate(), mimetype='text/plain')
    r.headers.set('Content-Disposition', 'attachment', filename=filename)
    return r


if __name__ == '__main__':
    port_run = int(os.environ.get("PORT", PORT))
    app.run(host=HOST, port=port_run, debug=DEBAG)
