from .. import __version__
from ..search import search as _search
from ..common import format_message
from ..log import list_logs, log_path, logfile

from flask import Flask, abort, Response, request
from jinja2 import Environment, FileSystemLoader

from collections import namedtuple
from httplib import NOT_FOUND
from os.path import dirname, realpath, join, isfile, basename
import logging

static_dir = join(dirname(realpath(__file__)), 'static')
get_template = Environment(loader=FileSystemLoader(static_dir)).get_template

Result = namedtuple('Result', ['log', 'text'])
app = Flask(__name__)


def supress_stdout_logs():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)


@app.route('/')
def index():
    template = get_template('index.html')
    logs = list_logs()
    return template.render(version=__version__, logs=logs)


@app.route('/log/<name>')
def log(name):
    path = log_path(name)
    if not isfile(path):
        abort(NOT_FOUND)

    with open(path) as fo:
        return Response(fo.read(), mimetype='text/plain')


@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    query = ''

    if request.method == 'POST':
        try:
            query = request.form['query'].strip()
            messages = _search(query)
            results = [Result(basename(logfile(msg.time)), format_message(msg))
                       for msg in messages]
        except Exception as err:
            error = str(err)
    else:
        results = None

    template = get_template('search.html')
    return template.render(
        version=__version__,
        results=results,
        error=error,
        query=query,
    )


def run():
    supress_stdout_logs()
    app.run(host='0.0.0.0')
