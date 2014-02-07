#!/bin/bash
# Test installation, this is done in bash since it's easier that way

root=/tmp/logbot-install-$(whoami)-$(hostname)

# Fail on first error
set -e
rm -rf ${root}
virtualenv-2.7 ${root}
. ${root}/bin/activate
python setup.py install
${root}/bin/logbot --help
