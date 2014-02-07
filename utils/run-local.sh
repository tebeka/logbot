#!/bin/bash
# Assumed that you have running openfire on localhost with password of 1234

. ./venv/bin/activate

host=$(hostname)

PYTHONPATH=${PWD} python -m logbot \
    --host ${host} \
    --user logbot \
    --passwd 1234 \
    --no-tls \
    biteam@conference.${host}
