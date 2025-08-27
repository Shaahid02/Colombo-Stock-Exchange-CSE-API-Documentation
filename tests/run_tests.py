#!/usr/bin/env python3
"""
Test runner for CSE API tests
Run all tests or specific test files
"""

import os
import sys
import importlib.util
import traceback
from pathlib import Path

def run_test_file(test_file):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"Running: {test_file}")
    print('='*60)
    
    try:
        # Add parent directory to path
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
        
        # Load and run the test module
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        # Try to run main function if it exists
        if hasattr(test_module, '__main__') or '__name__' in test_module.__dict__:
            # Execute the module's main code by running it again
            exec(open(test_file).read(), test_module.__dict__)
        
        print(f"✅ {test_file} completed successfully")
        return True
        
    except KeyboardInterrupt:
        print(f"⏹️  {test_file} interrupted by user")
        return False
    except Exception as e:
        print(f"❌ {test_file} failed with error:")
        print(f"   {str(e)}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all test files in the tests directory"""
    tests_dir = Path(__file__).parent
    test_files = list(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("No test files found in tests directory")
        return
    
    print(f"Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"  - {test_file.name}")
    
    results = {}
    total_tests = len(test_files)
    passed_tests = 0
    
    for test_file in test_files:
        try:
            success = run_test_file(test_file)
            results[test_file.name] = "PASSED" if success else "FAILED"
            if success:
                passed_tests += 1
        except KeyboardInterrupt:
            print(f"\n⏹️  Test run interrupted by user")
            break
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print()
    
    for test_name, result in results.items():
        status_icon = "✅" if result == "PASSED" else "❌"
        print(f"{status_icon} {test_name}: {result}")

def main():
    """Main function"""
    tests_dir = Path(__file__).parent
    
    if len(sys.argv) > 1:
        # Run specific test file
        test_name = sys.argv[1]
        if not test_name.startswith("test_"):
            test_name = f"test_{test_name}"
        if not test_name.endswith(".py"):
            test_name = f"{test_name}.py"
        
        test_file = tests_dir / test_name
        
        if test_file.exists():
            run_test_file(test_file)
        else:
            print(f"Test file not found: {test_file}")
            print("Available tests:")
            for test_file in tests_dir.glob("test_*.py"):
                print(f"  - {test_file.name}")
    else:
        # Run all tests
        run_all_tests()

if __name__ == "__main__":
    main()
