.DEFAULT_GOAL := help

.PHONY: help setup-dev

help:
	@echo "Available targets:"
	@echo "  setup-dev   - Set up the development environment with pre-commit hooks."

setup-dev:
	@echo "Setting up development environment..."
	@echo "==============================================================="
	pre-commit install
	@echo "Development environment setup complete."

setup-env:
	@echo "Setting up environment variables..."
	@echo "==============================================================="
	# Add any environment variable setup commands here
	@echo "Environment variables setup complete."

run: setup-env
	@echo "Running application..."
	@echo "==============================================================="
	cd apps/task-board && python3 app.py
