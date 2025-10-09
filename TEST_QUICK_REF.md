# Quick Test Reference

## Run Tests

```bash
pytest                          # All tests
pytest -v                       # Verbose
pytest -vv                      # Very verbose
pytest --cov=app               # With coverage
pytest --cov=app --cov-report=html  # HTML coverage report
```

## Run Specific Tests

```bash
pytest tests/test_api.py                                    # One file
pytest tests/test_api.py::TestBlacklistEndpoints           # One class
pytest tests/test_api.py::TestBlacklistEndpoints::test_add_blacklist_success  # One test
pytest -k "add_blacklist"                                   # Match test name
```

## Windows PowerShell

```powershell
.\run_tests.ps1                 # All tests
.\run_tests.ps1 -Coverage       # With coverage
.\run_tests.ps1 api             # API tests only
.\run_tests.ps1 -Verbose        # Verbose output
.\run_tests.ps1 -Help           # Show help
```

## Coverage Reports

```bash
pytest --cov=app --cov-report=term-missing   # Terminal with missing lines
pytest --cov=app --cov-report=html           # HTML report (htmlcov/index.html)
pytest --cov=app --cov-report=xml            # XML for CI/CD
```

## Test Markers

```bash
pytest -m unit                  # Unit tests only
pytest -m integration           # Integration tests only
pytest -m "not slow"           # Exclude slow tests
```

## Useful Options

```bash
pytest -x                       # Stop on first failure
pytest --lf                     # Run last failed tests
pytest --ff                     # Run failed tests first
pytest -s                       # Show print statements
pytest --tb=short              # Short traceback
pytest --tb=no                 # No traceback
pytest --collect-only          # Show tests without running
```

## Docker

```bash
docker-compose run --rm web pytest
docker-compose run --rm web pytest --cov=app
```

## Clean Up

```bash
rm -rf .pytest_cache htmlcov .coverage coverage.xml
find . -type d -name __pycache__ -exec rm -rf {} +
```

## View Results

- **Coverage HTML:** Open `htmlcov/index.html` in browser
- **Test Output:** Displayed in terminal
- **CI Results:** Check GitHub Actions tab

## Common Issues

**Tests not found:**
```bash
pytest --collect-only           # Verify test discovery
```

**Import errors:**
```bash
pip install -r requirements.txt
```

**Coverage not working:**
```bash
pip install pytest-cov
```
