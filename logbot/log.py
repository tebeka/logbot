'''Logs are in <log-dir>/<room>/<YYYYMMDD>.txt'''
from .common import format_message, logs_dir

from glob import glob
from os.path import join, basename, isdir

time_fmt = '%Y%m%d'


def log_path(room, log):
    return join(logs_dir, room, log)


def logfile(room, time):
    return log_path(room, '{}.txt'.format(time.strftime(time_fmt)))


def log(msg):
    filename = logfile(msg.room, msg.time)
    with open(filename, 'at') as out:
        out.write('{}\n'.format(format_message(msg)))


def iter_logs(room):
    return (basename(path) for path in glob(join(logs_dir, room, '*.txt')))


def iter_rooms():
    return (basename(path) for path in glob(join(logs_dir, '*'))
            if isdir(path))
