VENV=.venv
PYTHON=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip3
CODE_DIRS=dicomanonymizer tests

init:
	python3 -m venv $(VENV)
	$(PIP) install .[dev]

clean:
	rm -rf $(VENV)

test:
	$(PYTHON) -m pytest tests -rs

format:
	$(PYTHON) -m ruff format $(CODE_DIRS)

check:
	$(MAKE) format
	$(MAKE) test

reset:
	$(MAKE) clean
	$(MAKE) init
	$(MAKE) check