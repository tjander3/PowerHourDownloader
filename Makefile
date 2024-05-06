# TODO make clean for package
.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8 lint/black
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

# TODO make env will make an evrionemnt for you
# TODO verify this works in onjucutin with env-youtubedl
env: ## Make env need to provide name
	echo hi
	python -m venv ph
	#. ./ph/bin/activate
	. ./ph/Scripts/activate
	python -m pip install -r requirements_dev.txt

env-youtube:  ## Add youtube-dl
	mkdir included-sw
	git clone https://github.com/ytdl-org/youtube-dl.git included-sw/youtube-dl
	#git checkout aaed4884ed9954b8b69c3ca5254418ec578ed0b9  # TODO is something like this needed
	#python setup.py develop
	# TODO left off here why is it installying phd and not youtbedl
	pip install -e included-sw/youtube-dl

lint/flake8: ## check style with flake8
	flake8 powerhourdownloader tests
lint/black: ## check style with black
	black --check powerhourdownloader tests

lint: lint/flake8 lint/black ## check style

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source powerhourdownloader -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/powerhourdownloader.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ powerhourdownloader
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

package: install
	# Adding -w will remove cmd opening
	. ./ph/Scripts/activate; cd powerhourdownloader/webapp/; pyinstaller --paths . --paths ../../included-sw/youtube-dl -F --add-data "templates;templates" ./power_hour_downloader.py

install: clean ## install the package to the active Python's site-packages
	. ./ph/Scripts/activate
	python setup.py install

run: #install
	. ./ph/Scripts/activate
	cd powerhourdownloader/webapp/; export FLASK_APP=power_hour_downloader.py; flask run

debug: #install
	. ./ph/Scripts/activate
	cd powerhourdownloader/webapp/; export DEBUG=True;export FLASK_APP=power_hour_downloader.py; flask run

