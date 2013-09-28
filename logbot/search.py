from . import common
from .common import Message

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser

from glob import glob
from operator import itemgetter
from os import makedirs
from os.path import join, isdir
from sys import version_info

if version_info[0] >= 3:
    unicode = lambda x: x


schema = Schema(
    content=TEXT(stored=True),
    user=ID(stored=True),
    time=DATETIME(stored=True),
)


def open_index(path):
    if len(glob(join(path, '*.toc'))) > 0:
        return open_dir(path)

    if not isdir(path):
        makedirs(path)
    return create_in(path, schema)


def index(msg):
    ix = open_index(common.idx_dir)
    writer = ix.writer()
    writer.add_document(
        content=unicode(msg.content),
        user=unicode(msg.user),
        time=msg.time)
    writer.commit()


def search(query):
    ix = open_index(common.idx_dir)
    qparser = QueryParser('content', ix.schema)  # FIXME: Search all fields
    get_fields = itemgetter(*Message._fields)

    with ix.searcher() as searcher:
        query = qparser.parse(query)
        results = searcher.search(query, limit=100)
        # We need to create a list since searcher closes when we return - no
        # access to results
        return [Message._make(get_fields(res)) for res in results]
