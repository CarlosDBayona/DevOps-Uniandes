"""
Quick verification test.
Run this to verify the test setup is working correctly.
"""
import subprocess
import sys


def test_pytest_installed():
    """Verify pytest is installed."""
    try:
        import pytest
        print("✓ pytest is installed")
        print(f"  Version: {pytest.__version__}")
        return True
    except ImportError:
        print("✗ pytest is NOT installed")
        print("  Run: pip install -r requirements.txt")
        return False


def test_coverage_installed():
    """Verify pytest-cov is installed."""
    try:
        import pytest_cov
        print("✓ pytest-cov is installed")
        return True
    except ImportError:
        print("✗ pytest-cov is NOT installed")
        print("  Run: pip install pytest-cov")
        return False


def test_flask_installed():
    """Verify Flask is installed."""
    try:
        import flask
        print("✓ Flask is installed")
        print(f"  Version: {flask.__version__}")
        return True
    except ImportError:
        print("✗ Flask is NOT installed")
        return False


def test_app_importable():
    """Verify app module is importable."""
    try:
        from app import create_app
        print("✓ App module is importable")
        return True
    except ImportError as e:
        print(f"✗ App module import failed: {e}")
        return False


def count_tests():
    """Count available tests."""
    try:
        result = subprocess.run(
            ['pytest', '--collect-only', '-q'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout
        lines = output.strip().split('\n')
        
        for line in lines:
            if 'test' in line.lower():
                print(f"✓ Test discovery successful")
                print(f"  {line.strip()}")
                return True
        
        print("✗ No tests found")
        return False
    except Exception as e:
        print(f"✗ Test collection failed: {e}")
        return False


def run_sample_test():
    """Run a quick test."""
    try:
        print("\nRunning sample test...")
        result = subprocess.run(
            ['pytest', 'tests/test_models.py::TestBlacklistModel::test_blacklist_repr', '-v'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✓ Sample test PASSED")
            return True
        else:
            print("✗ Sample test FAILED")
            print(result.stdout)
            return False
    except Exception as e:
        print(f"✗ Could not run test: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Flask Blacklist API - Test Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Pytest Installation", test_pytest_installed),
        ("Coverage Plugin", test_coverage_installed),
        ("Flask Installation", test_flask_installed),
        ("App Module", test_app_importable),
        ("Test Discovery", count_tests),
    ]
    
    results = []
    for name, check in checks:
        print(f"\nChecking: {name}")
        print("-" * 40)
        success = check()
        results.append((name, success))
    
    # Run sample test
    print("\n" + "=" * 60)
    sample_success = run_sample_test()
    results.append(("Sample Test", sample_success))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status:8} {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Test setup is ready.")
        print("\nRun tests with:")
        print("  pytest")
        print("  pytest --cov=app")
        print("  .\\run_tests.ps1")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
