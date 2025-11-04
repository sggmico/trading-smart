.PHONY: help venv install install-dev test lint format clean run

VENV := venv
PYTHON_VERSION := 3.11
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip3

help:
	@echo "Available commands:"
	@echo "  make venv         - Create virtual environment"
	@echo "  make install      - Install dependencies"
	@echo "  make install-dev  - Install dev dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linting"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean temporary files"
	@echo "  make run          - Run the trading bot"

venv:
	@echo "Checking for Python $(PYTHON_VERSION)..."
	@if command -v python$(PYTHON_VERSION) >/dev/null 2>&1; then \
		python$(PYTHON_VERSION) -m venv $(VENV); \
		echo "Virtual environment created with Python $(PYTHON_VERSION)"; \
	else \
		echo "Python $(PYTHON_VERSION) not found. Using system python3..."; \
		python3 -m venv $(VENV); \
	fi
	@echo "Activate with: source $(VENV)/bin/activate"

install: venv
	$(PIP) install -r requirements.txt

install-dev: venv
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m flake8 src/ tests/
	$(PYTHON) -m mypy src/

format:
	$(PYTHON) -m black src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf $(VENV)

run:
	$(PYTHON) -m src.main
