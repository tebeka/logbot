from .common import format_message, logs_dir

from glob import glob
from os.path import join, basename


def log_path(log):
    return join(logs_dir, log)


def logfile(time):
    return log_path('{}.txt'.format(time.strftime('%Y%m%d')))


def log(msg):
    filename = logfile(msg.time)
    with open(filename, 'at') as out:
        out.write('{}\n'.format(format_message(msg)))


def list_logs():
    return sorted(basename(path) for path in glob(join(logs_dir, '*.txt')))
