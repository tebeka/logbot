#!/usr/bin/env python
'''Convert old (roomless) schema to new by adding a room to all documents
without one.
'''

from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(realpath(__file__))))

from logbot import common, search
from datetime import datetime
from getpass import getuser
from socket import gethostname

fix_id = 'd3a0e03c33d44b0886617b2c297fc0d7'


def mark_converted():
    msg = common.Message(
        content=fix_id,
        user=getuser(),
        room=gethostname(),
        time=datetime.now(),
    )
    search.index(msg)


def is_converted(ix):
    qparser = search.QueryParser('content', ix.schema)

    with ix.searcher() as searcher:
        query = qparser.parse(fix_id)
        results = searcher.search(query, limit=10)

        for _ in results:
            return True

    return False


def main(argv=None):
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('room', help='room name')
    args = parser.parse_args(argv[1:])

    room = args.room.decode('utf-8')
    ix = search.open_index(common.idx_dir)

    if is_converted(ix):
        raise SystemExit('error: already converted')

    count = 0
    for _, msg in ix.reader().iter_docs():
        if 'room' in msg:
            continue

        msg['room'] = room
        search.index(msg)
        count += 1

    mark_converted()
    print('Converted {} documents'.format(count))


if __name__ == '__main__':
    main()

