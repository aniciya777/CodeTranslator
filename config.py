import requests
import json
from parsers import python


HOST = '127.0.0.1'
PORT = 80
DEBAG = True
TRANSLATE_API_KEY = 'trnsl.1.1.20200312T083253Z.ed1eea08e54806bb.c8454d7a3f49ddd70d04ef91d585a889e21b3a3d'
LANGS = {}
DIRS = {}
PARSERS = {
    'python3': {
        'desc': 'Python 3',
        'files': {'py'},
        'parser': python.python_parser
    },
    'python2': {
        'desc': 'Python 2',
        'files': set(),
        'parser': python.python_parser
    },
}


def getLangs():
    global LANGS, DIRS
    params = {
        'key': TRANSLATE_API_KEY,
        'ui': 'ru'
    }
    response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/getLangs', params=params)
    if response.ok:
        response_json = json.loads(response.content)
        LANGS = response_json['langs']
        for s in response_json['dirs']:
            lang1, lang2 = s.split('-')
            if lang1 not in DIRS:
                DIRS[lang1] = set()
            DIRS[lang1].add(lang2)


getLangs()
print(LANGS)