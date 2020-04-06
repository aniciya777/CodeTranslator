from flask import Flask, render_template, request, redirect
from config import *
from functions import detect_lang, translate, replacer
from hashlib import md5
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    photo = FileField('Фото профиля')
    submit = SubmitField('Зарегистрироваться')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('register.html', form=form)


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
    app.run(host=HOST, port=PORT, debug=DEBAG)
