#!/bin/bash

export PYTHONPATH=${PWD}

. ./venv/bin/activate

python -m logbot \
    --host HOST \
    --user USER \
    --passwd PASSWD \
    --timezone "US/Pacific" \
    ROOM

# vim: ft=sh
