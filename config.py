import requests
import json
from parsers import python, text


HOST = '127.0.0.1'
PORT = 80
DEBAG = True
TRANSLATE_API_KEY = 'trnsl.1.1.20200312T083253Z.ed1eea08e54806bb.c8454d7a3f49ddd70d04ef91d585a889e21b3a3d'
DOWNLOAD_FILE_PATH = 'static/data/download/'
LIMIT_CHARS = 10000
LANGS = {}
LANGS_FROM = {}
DIRS = {}
DIR_JSON = ''
LANGS_JSON = ''
PARSERS = {
    'text': {
        'desc': 'Текст',
        'files': ['txt'],
        'parser': text.text_parser,
        'priority': 1.0,
    },
    'python3': {
        'desc': 'Python 3',
        'files': ['py'],
        'parser': python.python_parser,
        'priority': 1.0,
    },
    'python2': {
        'desc': 'Python 2',
        'files': ['py'],
        'parser': python.python_parser,
        'priority': 0.5,
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


getLangs()
print(DIRS)
print(LANGS)
