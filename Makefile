SHELL=/bin/bash
.DEFAULT_GOAL := _help

# NOTE: must put a <TAB> character and two pound "\t##" to show up in this list.  Keep it brief! IGNORE_ME
.PHONY: _help
_help:
	@grep -h "##" $(MAKEFILE_LIST) | grep -v IGNORE_ME | sed -e 's/##//' | column -t -s $$'\t'



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize venv, install requirements
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TODO: OS-independent venv, e.g. .venv/Scripts/activate
.PHONY: init
init:	## Initialize venv
	$(PY_SYS_INTERPRETER) -m venv --clear .venv
	$(PY_SYS_INTERPRETER) -m venv --upgrade-deps .venv
	- direnv allow


PYTHON ?= $(shell which python)
PWD ?= $(shell pwd)

.PHONY: _venv
_venv:
	# ensuring venv
	[ "${SKIP_VENV}" ] || [ "$(PYTHON)" = "$(PWD)/.venv/bin/python" ] || [ "$(PYTHON)" = "$(PWD)/.venv/Scripts/python" ]

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
CHANGED_FILES_PY_FLAG ?= $(shell if [ "$(CHANGED_FILES_PY)" ]; then echo 1; else echo; fi)

.PHONY: format
format: _venv	## Format the code
	if [ "${CHANGED_FILES_PY_FLAG}" ]; then \
	    isort ${CHANGED_FILES_PY}; \
	fi
	if [ "${CHANGED_FILES_PY_FLAG}" ]; then \
	    black ${CHANGED_FILES_PY}; \
	fi

.PHONY: lint
lint: _venv	## Lint the code
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Check formatting: Python
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	if [ "${CHANGED_FILES_PY_FLAG}" ]; then \
	    isort --diff --check ${CHANGED_FILES_PY}; \
	fi
	if [ "${CHANGED_FILES_PY_FLAG}" ]; then \
	    black --check ${CHANGED_FILES_PY}; \
	fi
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Lint Python
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	if [ "${CHANGED_FILES_PY_FLAG}" ]; then \
	    pycodestyle ${CHANGED_FILES_PY}; \
	fi
	if [ "${CHANGED_FILES_PY_FLAG}" ]; then \
	    bandit -c .banditrc -q -r ${CHANGED_FILES_PY}; \
	fi
	if [ "${CHANGED_FILES_PY_FLAG}" ]; then \
	    flake8 --statistics --doctests ${CHANGED_FILES_PY}; \
	fi
	if [ "${CHANGED_FILES_PY_FLAG}" ]; then \
	    pylint ${CHANGED_FILES_PY}; \
	fi
	if [ "${CHANGED_FILES_PY_FLAG}" ]; then \
	    mypy ${CHANGED_FILES_PY}; \
	fi

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

.PHONY: rank
rank:	## Rank (copy for google sheet)
	./cr fetch
	if [ "$(shell uname -o)" = "Darwin" ]; then \
		./cr rank --no-abbrev-titles -s -mg | pbcopy; \
	else \
		./cr rank --no-abbrev-titles -s -mg | xclip -sel clip; \
	fi



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verify targets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

N_ANNOTATED_FILES_ACTUAL ?= $(shell grep @author $(shell git ls-files \*.py) | wc -l)
N_ANNOTATED_FILES_EXPECT ?= $(shell git ls-files \*.py | grep -v glicko2 | wc -l)

.PHONY: verify/py-annotated
verify/py-annotated:	## Verify all python files have the annotation at top
	[[ "$(N_ANNOTATED_FILES_ACTUAL)" == "$(N_ANNOTATED_FILES_EXPECT)" ]]
