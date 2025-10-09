"""
Generate test statistics and summary.
"""
import os
import subprocess


def count_tests():
    """Count total number of tests."""
    result = subprocess.run(
        ['pytest', '--collect-only', '-q'],
        capture_output=True,
        text=True
    )
    output = result.stdout
    for line in output.split('\n'):
        if 'test' in line.lower() and 'selected' in line.lower():
            return line
    return "Unable to count tests"


def run_coverage():
    """Run tests with coverage and display summary."""
    print("Running tests with coverage...\n")
    subprocess.run(['pytest', '--cov=app', '--cov-report=term'])


def main():
    """Main function."""
    print("=" * 60)
    print("Flask Blacklist API - Test Statistics")
    print("=" * 60)
    print()
    
    # Count tests
    print("Test Count:")
    print(count_tests())
    print()
    
    # List test files
    test_files = []
    for root, dirs, files in os.walk('tests'):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                test_files.append(file)
    
    print(f"Test Files ({len(test_files)}):")
    for f in sorted(test_files):
        print(f"  - {f}")
    print()
    
    # Run coverage
    run_coverage()


if __name__ == '__main__':
    main()
