.PHONY: clean test integration-test all-tests docs swagger

SHELL = /bin/bash

default: bin/buildout

bin/python:
	virtualenv .  --no-site-packages
	bin/pip install --upgrade setuptools
	bin/pip install --upgrade pip
	bin/pip install wheel
	bin/pip install --use-wheel pycrypto certifi==2015.4.28
	# certifi==2015.4.28 https://github.com/kennethreitz/requests/issues/3212
	# Browsers and certificate authorities have concluded that 1024-bit
	# keys are unacceptably weak for certificates, particularly root certificates.
	# For this reason, Mozilla has removed any weak (i.e. 1024-bit key) certificate
	# from its bundle, replacing it with an equivalent strong
	# (i.e. 2048-bit or greater key) certificate from the same CA.

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

docs:
	bin/sphinx-apidoc -f -o api/docs/source -H "API Documentation" .
	bin/sphinx-build -b html -d documentation/html/doctrees -D latex_paper_size=a4 api/docs documentation/html
	@echo
	@echo "Build finished. The HTML pages are in documentation."

swagger:
	rm -rf documentation/swagger/schema
	cp -r api/schema documentation/swagger/schema
	@echo
	@echo "Swagger schema has been copied to documentation."
