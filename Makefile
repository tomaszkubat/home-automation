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
