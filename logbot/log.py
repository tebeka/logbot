from .common import format_message, logs_dir

from glob import glob
from os.path import join, basename

_log = _logfile = None


def log_for_time(time):
    return time.strftime('%Y%m%d.txt')


def get_log(time):
    global _log, _logfile

    logfile = log_path(log_for_time(time))
    if logfile != _logfile:
        if _log:
            _log.close()

        _logfile = logfile
        _log = open(logfile, 'at')

    return _log


def log(msg):
    out = get_log(msg.time)
    out.write('{}\n'.format(format_message(msg)))
    out.flush()


def list_logs():
    return sorted(basename(log) for log in glob(join(logs_dir, '*.txt')))


def log_path(log):
    return join(logs_dir, log)
