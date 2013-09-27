all:
	$(error Please pick a target)

test: clean
	flake8 logbot tests
	nosetests -vd tests

upload:
	python setup.py sdist upload

clean:
	rm -rf build dist logbot.egg-info/
	find . -name '*.py[co]' -exec rm -v {} \;

.PHONY: all test clean
