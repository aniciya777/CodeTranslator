from flask import Flask, render_template, request
from config import *
from functions import detect_lang, translate, replacer


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.files:
        f = request.files['files'].read()
        inputText = f.decode('utf-8')
    else:
        inputText = request.form.get('inputText', '').strip()
    lang1_key = request.form.get('inputGroupSelectLanguageFrom', '')
    lang2_key = request.form.get('inputGroupSelectLanguageTo', '')
    selectType = request.form.get('selectType', 'text'),
    outputText = ''
    parser = PARSERS[selectType[0]]
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
        'file_name': 'translate.' + parser['files'][0],
    }
    return render_template('index.html', **params)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBAG)
