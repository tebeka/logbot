from collections import namedtuple
from os import makedirs
from os.path import expanduser, join, isdir
from threading import Thread

cfg_dir = expanduser('~/.logbot')
idx_dir = join(cfg_dir, 'whoosh-db')
logs_dir = join(cfg_dir, 'logs')


Message = namedtuple('Message', ['content', 'user', 'time', 'room'])
listeners = []
format_message = '[{0.time:%H:%M}] <{0.user}> {0.content}'.format


def create_cfg_dirs(rooms):
    for dirname in (idx_dir, logs_dir):
        if not isdir(dirname):
            makedirs(dirname)

    for room in rooms:
        # biteam@archie -> biteam
        room = room.split('@')[0]
        room_dir = join(logs_dir, room)
        if not isdir(room_dir):
            makedirs(room_dir)


def run_thread(func, args=()):
    thr = Thread(target=func, args=args)
    thr.daemon = True
    thr.start()


def publish(msg):
    for func in listeners:
        func(msg)


def register_listener(func):
    listeners.append(func)
