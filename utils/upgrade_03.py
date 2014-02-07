#!/usr/bin/env python
'''Convert old (roomless) schema to new by adding a room to all documents
without one.
'''

from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(realpath(__file__))))

from glob import glob
from logbot import common, search
from os import rename, makedirs
from os.path import join, basename, isdir
from operator import itemgetter


get_values = itemgetter(*common.Message._fields)


def move_logs(room):
    room_dir = join(common.logs_dir, room)
    if not isdir(room):
        makedirs(room)

    count = 0
    for logfile in enumerate(glob(join(common.logs_dir, '*.txt')), 1):
        new_log = join(room_dir, basename(logfile))
        rename(logfile, new_log)

    return count


def convert_index(old_idx_dir, room):
    rename(common.idx_dir, old_idx_dir)
    ix = search.open_index(old_idx_dir)
    count = 0
    for count, (_, doc) in enumerate(ix.reader().iter_docs(), 1):
        if 'room' not in doc:
            doc['room'] = room
        msg = common.Message._make(get_values(doc))
        search.index(msg)

    return count


def main(argv=None):
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('room', help='room name')
    args = parser.parse_args(argv[1:])

    room = args.room.decode('utf-8')
    old_idx_dir = common.idx_dir + '.old'
    if isdir(old_idx_dir):
        raise SystemExit('error: {} already exists'.format(old_idx_dir))

    print('moving log files')
    nlogs = move_logs(args.room)
    print('moved {} logs'.format(nlogs))

    print('converting index')
    ndocs = convert_index(old_idx_dir, room)

    print('converted {} documents'.format(ndocs))
    print('Done. (old index at {})'.format(old_idx_dir))


if __name__ == '__main__':
    main()
