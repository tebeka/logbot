import logbot

from setuptools import setup
from os import walk
from os.path import dirname, realpath, join
import re

# A comment is a line starting with # or --
is_comment = re.compile('^\s*(#|--).*').match


def load_requirements(fname):
    here = dirname(realpath(__file__))
    fname = join(here, fname)

    with open(fname) as fo:
        return [line.strip() for line in fo
                if not is_comment(line) and line.strip()]

def static_files():
    for root, _, files in walk('logbot/httpd/static'):
        for name in files:
            yield join(root, name)

setup(
    name='logbot',
    version=logbot.__version__,
    packages=['logbot', 'logbot.httpd'],
    install_requires=load_requirements('requirements.txt'),
    package_data={
        'logbot': ['httpd/*.html'] + list(static_files()),
    },
    entry_points={
        'console_scripts': [
            'logbot = logbot.__main__:main',
        ]
    },
    tests_require=load_requirements('test-requirements.txt'),
    test_suite = 'nose.collector',
)
