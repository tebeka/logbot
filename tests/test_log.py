from nose.tools import with_setup

from datetime import datetime
from getpass import getuser
from os import makedirs
from os.path import isfile, isdir, join
from shutil import rmtree
from socket import gethostname
from tempfile import gettempdir
from time import sleep

from logbot import log, common

tmp = gettempdir()
tmp_logs = join(tmp, 'logbot-logs-{}-{}'.format(getuser(), gethostname()))
_orig_logdir = log.logs_dir


def setup():
    if isdir(tmp_logs):
        rmtree(tmp_logs)
    makedirs(tmp_logs)


def tl_setup():
    log.logs_dir = tmp_logs


def tl_teardown():
    log.logs_dir = _orig_logdir


@with_setup(tl_setup, tl_teardown)
def test_log():
    content, user, time = 'hello', 'lassie', datetime.now()
    msg = common.Message(content=content, user=user, time=time)
    log.log(msg)

    sleep(0.1)
    filename = log.logfile(msg.time)
    assert isfile(filename), 'no log file ({})'.format(filename)

    with open(filename) as fo:
        data = fo.read()

    msg = common.format_message(msg)
    assert msg in data, 'missing message'


def test_log_path():
    filename = 'foo.txt'

    lp = log.log_path(filename)
    assert filename in lp, 'bad log path'


def test_logfile():
    time = datetime.now()
    filename = log.logfile(time)

    ts = time.strftime(log.time_fmt)
    assert ts in filename, 'bad file name'


@with_setup(tl_setup, tl_teardown)
def test_logs():
    logs = set('{}.txt'.format(i) for i in range(10))
    for name in logs:
        with open(join(tmp_logs, name), 'w') as out:
            out.write(name)

    log_list = log.list_logs()
    found = set(log_list) & logs
    assert found == logs, 'missing logs'
