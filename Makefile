VENV=.venv
PYTHON=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip3

init:
	python3 -m venv $(VENV)
	$(PIP) install .[dev]

clean:
	rm -rf $(VENV)

test:
	$(PYTHON) -m pytest tests -rs

reset:
	$(MAKE) clean
	$(MAKE) init
	$(MAKE) test