from nose import SkipTest

from os import environ
from os.path import dirname, realpath
from subprocess import call

if 'LOGBOT_TEST_INSTALL' not in environ:
    raise SkipTest


def test_install():
    root = dirname(dirname(realpath(__file__)))
    rv = call(['./tests/test-install.sh'], cwd=root)
    assert rv == 0, 'test-install.sh returned {}'.format(rv)
