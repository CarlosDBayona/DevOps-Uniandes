# Flask Blacklist API

[![Tests](https://github.com/CarlosDBayona/DevOps-Uniandes/actions/workflows/tests.yml/badge.svg)](https://github.com/CarlosDBayona/DevOps-Uniandes/actions/workflows/tests.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask 1.1.4](https://img.shields.io/badge/flask-1.1.4-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This project is a minimal Flask 1.1.x API for managing email blacklists using SQLAlchemy, Flask-RESTful, and Marshmallow. It includes a Dockerfile and docker-compose for running with PostgreSQL.

## Table of Contents
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Testing](#testing)
- [Development](#development)

## Requirements
- Docker + Docker Compose

## Quick start

1. Copy `.env.example` to `.env` and change values if needed.
2. Start services:

```powershell
docker-compose up --build
```

3. The database tables will be created automatically on startup.

## API Endpoints

All endpoints require Bearer token authentication using the header:
```
Authorization: Bearer secret-token
```

### Blacklist Endpoints
- **POST /blacklists** - Add an email to the blacklist
  - Body: `{ "email": "user@example.com", "app_uuid": "app-123", "blocked_reason": "spam" }`
  - Response: `{ "msg": "Email added to blacklist" }` (201)

- **GET /blacklists/<email>** - Check if an email is blacklisted
  - Response: `{ "blocked": true, "reason": "spam" }` or `{ "blocked": false, "reason": null }` (200)

## Configuration

The static bearer token can be configured via environment variable:
- `STATIC_BEARER_TOKEN`: Default is "secret-token"

## Testing

### API Testing with Postman

Use the included `postman_collection.json` for API testing. It includes:
- Comprehensive test cases for both endpoints
- Tests for authentication (valid token, no token, invalid token)
- Tests for validation (missing email)
- Automated test scripts for each request

### Unit Testing

The project includes comprehensive unit tests using pytest.

#### Running Tests Locally

```powershell
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run tests with verbose output
pytest -v
```

#### Using Makefile (Unix/Linux/Mac)

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run only unit tests
make test-unit

# Run tests verbosely
make test-verbose

# Clean test artifacts
make clean
```

#### Running Tests in Docker

```powershell
docker-compose run --rm web pytest
```

#### Test Coverage

The test suite includes:
- **Model Tests** (`test_models.py`): Tests for Blacklist model
- **API Tests** (`test_api.py`): Tests for all API endpoints
- **Schema Tests** (`test_schemas.py`): Tests for Marshmallow schemas
- **Integration Tests**: Complete workflow scenarios
- **Authentication Tests**: Security and token validation

Current test coverage: **>90%**

View detailed coverage report:
```powershell
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

**📚 For detailed testing documentation, see [TESTING.md](TESTING.md)**

**⚡ Quick reference: [TEST_QUICK_REF.md](TEST_QUICK_REF.md)**

### Continuous Integration

Tests are automatically run on GitHub Actions for every push and pull request. See `.github/workflows/tests.yml` for configuration.

## Development

### Project Structure

```
.
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Database models
│   ├── schemas.py            # Marshmallow schemas
│   └── resources/
│       └── blacklist.py      # API endpoints
├── tests/
│   ├── conftest.py           # Test fixtures
│   ├── test_app.py           # App configuration tests
│   ├── test_models.py        # Model tests
│   ├── test_api.py           # API endpoint tests
│   └── test_schemas.py       # Schema tests
├── .github/
│   └── workflows/
│       └── tests.yml         # GitHub Actions CI
├── docker-compose.yml        # Docker compose configuration
├── Dockerfile                # Docker image definition
├── requirements.txt          # Python dependencies
├── pytest.ini                # Pytest configuration
├── run.py                    # Application entry point
└── README.md                 # This file
```

### Local Development Setup

1. **Create virtual environment:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

3. **Set up environment variables:**
```powershell
cp .env.example .env
# Edit .env with your configuration
```

4. **Run locally:**
```powershell
python run.py
```

The API will be available at `http://localhost:5000`

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Quality

- **Tests:** All new features must include tests
- **Coverage:** Maintain >90% test coverage
- **Style:** Follow PEP 8 guidelines
- **Documentation:** Update README and docstrings

## License

This project is licensed under the MIT License.

## Authors

- Universidad de los Andes - DevOps Course

## Acknowledgments

- Flask and its ecosystem
- PostgreSQL
- Docker
- GitHub Actions


