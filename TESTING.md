# Testing Documentation

## Overview

This project includes a comprehensive test suite using **pytest** to ensure the reliability and correctness of the Flask Blacklist API.

## Test Structure

```
tests/
├── __init__.py           # Tests package initialization
├── conftest.py           # Pytest configuration and fixtures
├── test_app.py           # Application configuration tests
├── test_models.py        # Database model tests
├── test_api.py           # API endpoint tests
└── test_schemas.py       # Schema serialization tests
```

## Test Coverage

### 1. Model Tests (`test_models.py`)
Tests for the `Blacklist` model:
- Creating blacklist entries with all fields
- Creating entries with minimal required fields
- Model representation (`__repr__`)
- Querying entries by email
- Multiple entries for the same email
- Ordering by creation timestamp

**Coverage:** 100% of model code

### 2. API Endpoint Tests (`test_api.py`)

#### POST /blacklists Tests
- ✓ Successfully adding email to blacklist
- ✓ Adding with minimal data (email only)
- ✓ Missing required email field (400 error)
- ✓ Empty email string (400 error)
- ✓ No authentication token (401 error)
- ✓ Invalid authentication token (401 error)
- ✓ Malformed authorization header (401 error)
- ✓ No JSON body (400 error)

#### GET /blacklists/<email> Tests
- ✓ Checking existing blacklisted email
- ✓ Checking non-existent email
- ✓ Returns most recent entry for duplicate emails
- ✓ No authentication token (401 error)
- ✓ Invalid authentication token (401 error)
- ✓ Special characters in email address

#### Integration Tests
- ✓ Complete add-and-check workflow
- ✓ Multiple additions of same email
- ✓ Different emails tracked independently

#### Authentication Tests
- ✓ Token case sensitivity
- ✓ Bearer prefix requirement
- ✓ Extra spaces handling

**Coverage:** >95% of API code

### 3. Schema Tests (`test_schemas.py`)
Tests for Marshmallow schemas:
- Serializing blacklist entries
- Handling None values
- Deserializing JSON data
- Schema validation

**Coverage:** 100% of schema code

### 4. Application Tests (`test_app.py`)
Tests for Flask app configuration:
- Application creation
- Configuration settings
- Environment variables
- Database URI configuration
- Route registration
- Database table creation
- Error handling (404, 405)
- JSON response format

**Coverage:** 100% of app initialization code

## Fixtures

Defined in `conftest.py`:

### `app`
Provides a Flask application configured for testing with:
- In-memory SQLite database
- Testing mode enabled
- Test authentication token

### `client`
Provides a test client for making HTTP requests

### `auth_headers`
Provides valid authorization headers for authenticated requests

### `sample_blacklist`
Provides pre-populated blacklist entries for testing

## Running Tests

### Basic Usage

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run specific test class
pytest tests/test_api.py::TestBlacklistEndpoints

# Run specific test
pytest tests/test_api.py::TestBlacklistEndpoints::test_add_blacklist_success
```

### With Coverage

```bash
# Run with coverage report
pytest --cov=app

# Generate HTML coverage report
pytest --cov=app --cov-report=html

# View coverage in browser
# Open htmlcov/index.html
```

### With Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Verbose Output

```bash
# Verbose output
pytest -v

# Very verbose output
pytest -vv

# Show print statements
pytest -s
```

## Windows PowerShell Script

Use the provided `run_tests.ps1` script:

```powershell
# Run all tests
.\run_tests.ps1

# Run with coverage
.\run_tests.ps1 -Coverage

# Run API tests only
.\run_tests.ps1 api

# Run with verbose output
.\run_tests.ps1 -Verbose

# Show help
.\run_tests.ps1 -Help
```

## Continuous Integration

Tests run automatically on GitHub Actions for:
- Every push to `main` or `develop` branches
- Every pull request to `main` or `develop` branches
- Multiple Python versions (3.8, 3.9, 3.10)

See `.github/workflows/tests.yml` for CI configuration.

## Test Statistics

Run test statistics script:

```bash
python test_stats.py
```

This will show:
- Total number of tests
- Test files
- Coverage summary

## Writing New Tests

### Example Test Function

```python
def test_example(client, auth_headers):
    """Test example endpoint."""
    # Arrange
    data = {'email': 'test@example.com'}
    
    # Act
    response = client.post(
        '/blacklists',
        data=json.dumps(data),
        headers=auth_headers
    )
    
    # Assert
    assert response.status_code == 201
    assert response.json['msg'] == 'Email added to blacklist'
```

### Best Practices

1. **Use descriptive test names**: `test_add_blacklist_success` not `test_1`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **One assertion per test**: Focus on testing one thing
4. **Use fixtures**: Reuse common setup code
5. **Test edge cases**: Empty strings, None values, special characters
6. **Test error conditions**: Invalid input, auth failures
7. **Add docstrings**: Explain what the test verifies

## Coverage Goals

- **Overall Coverage:** >90%
- **Critical Paths:** 100% (authentication, data validation)
- **Models:** 100%
- **API Endpoints:** >95%

## Troubleshooting

### Tests Not Found

```bash
# Verify pytest can discover tests
pytest --collect-only
```

### Import Errors

```bash
# Install dependencies
pip install -r requirements.txt
```

### Database Errors

Tests use in-memory SQLite database. If you see database errors:
- Check that `SQLALCHEMY_DATABASE_URI` is set to `sqlite:///:memory:` in test config
- Ensure fixtures are properly cleaning up

### Coverage Not Generated

```bash
# Install coverage plugin
pip install pytest-cov
```

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/en/2.0.x/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
