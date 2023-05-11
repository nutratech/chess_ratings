SHELL=/bin/bash
.DEFAULT_GOAL := _help

# NOTE: must put a <TAB> character and two pound "\t##" to show up in this list.  Keep it brief! IGNORE_ME
.PHONY: _help
_help:
	@grep -h "##" $(MAKEFILE_LIST) | grep -v IGNORE_ME | sed -e 's/##//' | column -t -s $$'\t'



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize venv, install requirements
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TODO: OS-dependent venv
.PHONY: init
init:	## Initialize venv
	rm -rf .venv
	${PY_SYS_INTERPRETER}-m venv .venv
	${PY_SYS_INTERPRETER} -m venv --upgrade-deps .venv
	direnv allow


PYTHON ?= $(shell which python)
PWD ?= $(shell pwd)

.PHONY: _venv
_venv:
	# ensuring venv
	[ "${SKIP_VENV}" ] || [ "$(PYTHON)" = "$(PWD)/.venv/bin/python" ]

.PHONY: deps
deps: _venv	## Install requirements & sub-module
	git submodule update --init
	pip install -r requirements.txt
	- pip install -r requirements-lint.txt



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Lint, test, format, clean
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

REF_HEAD ?= origin/master
CHANGED_FILES_PY ?= $(shell git diff $(REF_HEAD) --name-only --diff-filter=MACRU \*.py)
# CHANGED_FILES_PY ?= cr setup.py chessdet/ tests/

.PHONY: format
format: _venv	## Format the code
ifneq ($(CHANGED_FILES_PY),)
	isort ${CHANGED_FILES_PY}
	black ${CHANGED_FILES_PY}
else
	@echo "No changed python files, skipping."
endif


.PHONY: lint
lint: _venv	## Lint the code
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Check formatting: Python
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ifneq ($(CHANGED_FILES_PY),)
	isort --diff --check ${CHANGED_FILES_PY}
	black --check ${CHANGED_FILES_PY}
else
	@echo "No changed python files, skipping."
endif
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Lint Python
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ifneq ($(CHANGED_FILES_PY),)
	pycodestyle ${CHANGED_FILES_PY}
	bandit -c .banditrc -q -r ${CHANGED_FILES_PY}
	flake8 --statistics --doctests ${CHANGED_FILES_PY}
	pylint ${CHANGED_FILES_PY}
	mypy ${CHANGED_FILES_PY}
else
	@echo "No changed python files, skipping."
endif

.PHONY: lint-all
lint-all:	## Lint all code (non-incremental)
	CHANGED_FILES_PY="cr setup.py chessdet/ tests/" make lint


.PHONY: test
test: _venv	## Test the code
	coverage run
	coverage report
	grep fail_under setup.cfg


ALL_CLEAN_LOCS=build/ *.egg-info
ALL_CLEAN_SCAN_LOCS=cr *.py chessdet/ tests/
ALL_CLEAN_ARGS=-name .coverage -o -name __pycache__ -o -name .pytest_cache -o -name .mypy_cache

.PHONY: clean
clean:	## Clean up pycache/ and other left overs
	rm -rf ${ALL_CLEAN_LOCS}
	rm -rf $(shell find . -maxdepth 1 $(ALL_CLEAN_ARGS))
	rm -rf $(shell find $(ALL_CLEAN_SCAN_LOCS) $(ALL_CLEAN_ARGS))



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Install, build
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PY_SYS_INTERPRETER ?= /usr/bin/python3

.PHONY: install
install:	## Install into user space
	$(PY_SYS_INTERPRETER) -m pip install .

.PHONY: build
build:	## Bundle a source distribution
	$(PY_SYS_INTERPRETER) setup.py sdist



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Rank
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UNAME_S ?= $(shell uname -s)

.PHONY: rank
rank:	## Rank (copy for google sheet)
	./cr fetch
ifeq ($(UNAME_S),Darwin)
	./cr rank --no-abbrev-titles -s -mg | pbcopy
else
	./cr rank --no-abbrev-titles -s -mg | xclip -sel clip
endif



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verify targets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

N_ANNOTATED_FILES_ACTUAL ?= $(shell grep @author $(shell git ls-files \*.py) | wc -l)
N_ANNOTATED_FILES_EXPECT ?= $(shell git ls-files \*.py | grep -v glicko2 | wc -l)

.PHONY: verify/py-annotated
verify/py-annotated:	## Verify all python files have the annotation at top
	[[ "$(N_ANNOTATED_FILES_ACTUAL)" == "$(N_ANNOTATED_FILES_EXPECT)" ]]
