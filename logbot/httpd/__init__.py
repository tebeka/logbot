from .. import __version__
from ..search import search as _search
from ..common import format_message
from ..log import iter_rooms, iter_logs, log_path, logfile

from flask import Flask, abort, Response, request, redirect, url_for
from jinja2 import Environment, FileSystemLoader

from collections import namedtuple
from os.path import dirname, realpath, join, isfile
import logging

from sys import version_info

if version_info[0] >= 3:
    from http.client import NOT_FOUND
else:
    from httplib import NOT_FOUND

here = dirname(realpath(__file__))
static_dir = join(here, 'static')
get_template = Environment(loader=FileSystemLoader(here)).get_template

Result = namedtuple('Result', ['msg', 'text'])
app = Flask(__name__)


def supress_stdout_logs():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)


@app.route('/')
def index():
    # Since we create room directories on startup, we'll always have at least
    # one room
    room = sorted(iter_rooms())[0]
    return redirect(url_for('room', room=room))


@app.route('/room/<room>')
def room(room):
    template = get_template('index.html')
    return template.render(version=__version__, current_room=room,
                           rooms=iter_rooms(), logs=iter_logs(room))


@app.route('/log/<room>/<name>')
def log(room, name):
    path = log_path(room, name)
    if not isfile(path):
        abort(NOT_FOUND)

    with open(path) as fo:
        return Response(fo.read(), mimetype='text/plain')


def msg_log_url(msg):
    name = logfile(msg, base_only=True)
    return url_for('log', room=msg.room, name=name)


@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    query = ''

    results = None
    if request.method == 'POST':
        try:
            query = request.form['query'].strip()
            results = _search(query)
        except Exception as err:
            error = str(err)

    template = get_template('search.html')
    return template.render(
        version=__version__,
        results=results,
        error=error,
        query=query,

        fmt=format_message,
        urlof=msg_log_url,
    )


def run():
    supress_stdout_logs()
    app.run(host='0.0.0.0')
