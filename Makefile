.PHONY: help run setup install clean

# Default target - run the application
.DEFAULT_GOAL := run

help:
	@echo "DJDownload - Available commands:"
	@echo "  make run      - Run the application (default)"
	@echo "  make setup    - Create virtual environment and install dependencies"
	@echo "  make install  - Install dependencies in existing venv"
	@echo "  make clean    - Remove virtual environment and cache files"

# Run the main application
run:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@venv/bin/python src/main.py

# Run the main application in prep mode
prep:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@venv/bin/python src/main.py -p

# Setup virtual environment and install dependencies
setup:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Installing dependencies..."
	venv/bin/pip install --upgrade pip
	venv/bin/pip install pydub mutagen
	@echo "Setup complete! Run 'make run' to start the application."

# Install dependencies in existing virtual environment
install:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	venv/bin/pip install pydub mutagen

# Clean up virtual environment and cache
clean:
	@echo "Cleaning up..."
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete."
