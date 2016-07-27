.PHONY: clean test integration-test all-tests

SHELL = /bin/bash

default: bin/buildout

bin/python:
	virtualenv .  --no-site-packages
	bin/pip install --upgrade setuptools
	bin/pip install --upgrade pip
	bin/pip install wheel pycrypto

bin/buildout: bin/python
	bin/python bootstrap.py -v 2.5.1

clean:
	# virtualenv
	rm -Rf bin include lib local
	# buildout and pip
	rm -Rf develop-eggs eggs *.egg-info
	rm -Rf src parts build dist
	rm -Rf .installed.cfg pip-selfcheck.json
	# tests' cache
	rm -Rf .cache tests/.cache
	rm -Rf tests/integration/__pycache__ tests/integration/.cache
	rm -Rf tests/test_api/__pycache__ tests/test_api/.cache

test:
	bin/py.test -m 'not ignore' --pep8 --cov api --cov-report term-missing tests/test_api

integration-test:
	bin/py.test -m 'integration and not ignore' --pep8 tests/integration

all-tests:
	bin/py.test -m 'not ignore' --pep8 tests/test_api
	bin/py.test -m 'integration and not ignore' --pep8 tests/integration
