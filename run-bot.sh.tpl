#!/bin/bash

export PYTHONPATH=${PWD}

. ./venv/bin/activate

python logbot/__main__.py \
    --host ##HOST## \
    --user ##USER## \
    --passwd ##PASS## \
    --timezone "US/Pacific" \
    ##ROOM##
