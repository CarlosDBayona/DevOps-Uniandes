# Flask Blacklist API - Test Runner
# PowerShell script for running tests on Windows

param(
    [Parameter(Position=0)]
    [string]$TestType = "all",
    
    [switch]$Coverage,
    [switch]$Verbose,
    [switch]$Help
)

function Show-Help {
    Write-Host "Flask Blacklist API - Test Runner" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\run_tests.ps1 [TestType] [-Coverage] [-Verbose] [-Help]"
    Write-Host ""
    Write-Host "TestType options:"
    Write-Host "  all           Run all tests (default)"
    Write-Host "  unit          Run unit tests only"
    Write-Host "  integration   Run integration tests only"
    Write-Host "  models        Run model tests only"
    Write-Host "  api           Run API tests only"
    Write-Host "  schemas       Run schema tests only"
    Write-Host ""
    Write-Host "Flags:"
    Write-Host "  -Coverage     Generate coverage report"
    Write-Host "  -Verbose      Show verbose output"
    Write-Host "  -Help         Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\run_tests.ps1                    # Run all tests"
    Write-Host "  .\run_tests.ps1 -Coverage          # Run with coverage"
    Write-Host "  .\run_tests.ps1 api -Verbose       # Run API tests verbosely"
    Write-Host "  .\run_tests.ps1 unit -Coverage     # Run unit tests with coverage"
    Write-Host ""
}

if ($Help) {
    Show-Help
    exit 0
}

Write-Host "Flask Blacklist API - Running Tests..." -ForegroundColor Green
Write-Host ""

# Build pytest command
$pytestCmd = "pytest"

# Add test selection
switch ($TestType.ToLower()) {
    "unit" {
        $pytestCmd += " -m unit"
        Write-Host "Running: Unit Tests" -ForegroundColor Yellow
    }
    "integration" {
        $pytestCmd += " -m integration"
        Write-Host "Running: Integration Tests" -ForegroundColor Yellow
    }
    "models" {
        $pytestCmd += " tests/test_models.py"
        Write-Host "Running: Model Tests" -ForegroundColor Yellow
    }
    "api" {
        $pytestCmd += " tests/test_api.py"
        Write-Host "Running: API Tests" -ForegroundColor Yellow
    }
    "schemas" {
        $pytestCmd += " tests/test_schemas.py"
        Write-Host "Running: Schema Tests" -ForegroundColor Yellow
    }
    default {
        Write-Host "Running: All Tests" -ForegroundColor Yellow
    }
}

# Add coverage if requested
if ($Coverage) {
    $pytestCmd += " --cov=app --cov-report=html --cov-report=term-missing"
    Write-Host "Coverage: Enabled" -ForegroundColor Yellow
}

# Add verbose if requested
if ($Verbose) {
    $pytestCmd += " -vv"
    Write-Host "Verbosity: High" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Command: $pytestCmd" -ForegroundColor Cyan
Write-Host ""

# Run tests
Invoke-Expression $pytestCmd

$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "Tests Passed! ✓" -ForegroundColor Green
    
    if ($Coverage) {
        Write-Host ""
        Write-Host "Coverage report generated in: htmlcov\index.html" -ForegroundColor Cyan
    }
} else {
    Write-Host "Tests Failed! ✗" -ForegroundColor Red
}

exit $exitCode
