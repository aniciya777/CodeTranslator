from flask import Flask, render_template
from config import *


app = Flask(__name__)


@app.route('/')
def index():
    params = {
        'PARSERS': PARSERS,
        'LANGS': LANGS
    }
    return render_template('index.html', **params)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBAG)
