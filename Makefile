SHELL := $(shell which bash)
ACTIVATE_VENV = source venv/bin/activate
PYTHONPATH = $(shell pwd)

all:
	$(error Please pick a target)

test: clean
	flake8 logbot tests
	nosetests -vd tests

upload:
	python setup.py sdist upload

clean:
	rm -rf build dist logbot.egg-info/
	-find logbot -name __pycache__ -exec rm -rfv {} \;
	-find tests -name __pycache__ -exec rm -rfv {} \;
	-find tests -name '*.py[co]' -exec rm -v {} \;
	-find logbot -name '*.py[co]' -exec rm -v {} \;

github:
	hg bookmark -r default master
	hg push git+ssh://git@github.com/tebeka/logbot.git

start-supervisor:
	test -d logs || mkdir logs
	${ACTIVATE_VENV} && supervisord

start:
	${ACTIVATE_VENV} && supervisorctl start all

stop:
	${ACTIVATE_VENV} && supervisorctl stop all


.PHONY: all test clean start
