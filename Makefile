.PHONY: test test-cov test-unit test-integration test-verbose install clean help

help:
	@echo "Flask Blacklist API - Available commands:"
	@echo ""
	@echo "  make install          Install dependencies"
	@echo "  make test             Run all tests"
	@echo "  make test-cov         Run tests with coverage report"
	@echo "  make test-unit        Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make test-verbose     Run tests with verbose output"
	@echo "  make clean            Clean test artifacts"
	@echo "  make docker-test      Run tests in Docker"
	@echo ""

install:
	pip install -r requirements.txt

test:
	pytest

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-verbose:
	pytest -vv

clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-test:
	docker-compose run --rm web pytest
