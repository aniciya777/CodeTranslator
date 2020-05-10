import requests
import json
from parsers import python, text
from data import db_session
from data.languages import Languages
from data.code_languages import CodeLanguages


db_session.global_init("db/database.sqlite")
session = db_session.create_session()
HOST = '0.0.0.0'
PORT = 80
DEBAG = False
SECRET_KEY = 'translate_key'
TRANSLATE_API_KEY = 'trnsl.1.1.20200312T083253Z.ed1eea08e54806bb.c8454d7a3f49ddd70d04ef91d585a889e21b3a3d'
DOWNLOAD_FILE_PATH = 'static/data/download/'
AVATARS_SAVE_PATH = 'static/img/avatars'
MAX_CONTENT_LENGTH = 2 * 1024 * 1024
LIMIT_CHARS = 10000
MIN_PASSWORD_LENGTH = 8
MAX_TRANSLATIONS_IN_HISTORY_FOR_USER = 30
LANGS = {}
LANGS_FROM = {}
DIRS = {}
DIR_JSON = ''
LANGS_JSON = ''
PARSERS = {
    'text': {
        'files': ['txt'],
        'parser': text.text_parser,
        'priority': 1.0,
        'db_record': session.query(CodeLanguages).get(1),
    },
    'python3': {
        'files': ['py'],
        'parser': python.python_parser,
        'priority': 1.0,
        'db_record': session.query(CodeLanguages).get(2),
    },
    'python2': {
        'files': ['py'],
        'parser': python.python_parser,
        'priority': 0.5,
        'db_record': session.query(CodeLanguages).get(3),
    },
}


def getLangs():
    global LANGS, DIRS, LANGS_FROM, DIR_JSON, LANGS_JSON
    params = {
        'key': TRANSLATE_API_KEY,
        'ui': 'ru'
    }
    try:
        response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/getLangs', params=params)
        if response.ok:
            response_json = json.loads(response.content)
            LANGS = response_json['langs']
            for s in response_json['dirs']:
                lang1, lang2 = s.split('-')
                if lang1 not in DIRS:
                    DIRS[lang1] = set()
                DIRS[lang1].add(lang2)
        else:
            raise BaseException
    except BaseException:
        print('Ошибка загрузки списка языков')
        dirs_list = json.load(open('static/data/dirs.json'))
        DIRS = {key: set(value) for key, value in dirs_list.items()}
        LANGS = json.load(open('static/data/langs.json'))
    finally:
        LANGS_FROM = {key: value for key, value in LANGS.items() if key in DIRS}
        dirs_list = {key: list(value) for key, value in DIRS.items()}
        try:
            json.dump(dirs_list, open('static/data/dirs.json', 'w'))
        except FileNotFoundError:
            print('Ошибка записи dirs.json')
        DIR_JSON = '{\n'
        for key, value in DIRS.items():
            temp = ', '.join(f'`{s}`' for s in value)
            DIR_JSON += f'{key}: [{temp}], '
        DIR_JSON += '\n}'
        LANGS_JSON = '{\n'
        for key, value in LANGS.items():
            LANGS_JSON += f'{key}: `{value}`, '
        LANGS_JSON += '\n}'
        try:
            json.dump(LANGS, open('static/data/langs.json', 'w'))
        except FileNotFoundError:
            print('Ошибка записи langs.json')
        # Сохранение в БД
        session = db_session.create_session()
        for key, value in LANGS.items():
            try:
                new_lang = Languages(
                    code=key,
                    title=value
                )
                session.add(new_lang)
                session.commit()
            except BaseException:
                pass


getLangs()
print(DIRS)
print(LANGS)
