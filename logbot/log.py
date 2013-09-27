from .common import format_message, logs_dir

from glob import glob
from os.path import join, basename

time_fmt = '%Y%m%d'


def log_path(log):
    return join(logs_dir, log)


def logfile(time):
    return log_path('{}.txt'.format(time.strftime(time_fmt)))


def log(msg):
    filename = logfile(msg.time)
    with open(filename, 'at') as out:
        out.write('{}\n'.format(format_message(msg)))


def list_logs():
    return sorted(basename(path) for path in glob(join(logs_dir, '*.txt')))
