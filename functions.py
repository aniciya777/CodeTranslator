import requests
from config import *


def detect_lang(data):
    text = '\n'.join(map(lambda obj:obj['comment'], data))
    try:
        response = requests.post('https://translate.yandex.net/api/v1.5/tr.json/detect', params={
            'key': TRANSLATE_API_KEY,
            'text': text
        })
        if response:
            response_json = response.json()
            if response_json['code'] == 200:
                return response_json['lang']
        return 'ru'
    except BaseException:
        return 'ru'


def translate(data, lang_from, lang_to):
    text = [obj['comment'] for obj in data]
    translated_text = [''] * len(text)
    try:
        response = requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate', params={
            'key': TRANSLATE_API_KEY,
            'text': text[:LIMIT_CHARS],
            'lang': f'{lang_from}-{lang_to}',
            'format': 'plain'
        })
        if response:
            response_json = response.json()
            if response_json['code'] == 200:
                translated_text = response_json['text']
    finally:
        for i in range(len(data)):
            data[i]['translated_comment'] = translated_text[i]
        return data

def replacer(text, data):
    text = text.splitlines()
    data = sorted(data, key=lambda x: x['to'], reverse=True)
    for item in data:
        row = item['from'][0]
        start = item['from'][1]
        end = item['to'][1]
        s = item['translated_comment']
        try:
            text[row] = text[row][:start] + s + text[row][end:]
        except BaseException:
            pass
    text = '\r\n'.join(text)
    return text
