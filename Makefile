.DEFAULT_GOAL: help
.PHONY: help setup-dev setup-env clean-env run-dev run-prod

VENV_DIR := .venv

help:
	@echo "Available targets:"
	@echo ""
	@echo "RUNNING AN APPLICATION:"
	@echo "  run-dev     - run the application in development mode."
	@echo "  run-prod    - run the application in production mode."
	@echo ""
	@echo "SETTING UP ENVIRONMENT:"
	@echo "  setup-dev   - set up the environment to develop an application."
	@echo "  setup-env   - set up the environment to run an application."
	@echo "  clean-env   - clean the environment."
	@echo ""

setup-dev: setup-env
	@echo "Setting up development environment..."
	@echo "==============================================================="
	pre-commit install
	@echo "Development environment setup completed."

setup-env:
	@echo "Setting up environment ..."
	@echo "==============================================================="
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
	fi
	@echo "Installing dependencies..."
	@$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Environment setup completed."

clean-env:
	@echo "Cleaning environment..."
	@echo "==============================================================="
	rm -rf $(VENV_DIR)
	@echo "Environment cleaned."

run-dev: setup-env
	@echo "Running application..."
	@echo "==============================================================="
	cd apps/task-board && python3 app.py

run-prod: setup-env
	@echo "Running application..."
	@echo "==============================================================="
	cd apps/task-board && ../../$(VENV_DIR)/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app
