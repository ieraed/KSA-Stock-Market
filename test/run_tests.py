#!/usr/bin/env python3
"""
Unified Test Runner for Saudi Stock Market App
Run all tests or specific categories
"""

import sys
import os
import importlib.util
import argparse
from pathlib import Path

def run_test_file(test_path):
    """Run a single test file"""
    test_name = test_path.stem
    
    try:
        print(f"\n{'='*50}")
        print(f"🧪 RUNNING: {test_name}")
        print(f"{'='*50}")
        
        # Import and run the test
        spec = importlib.util.spec_from_file_location(test_name, test_path)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        print(f"✅ {test_name} completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ {test_name} failed: {str(e)}")
        return False

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description='Run Saudi Stock Market App tests')
    parser.add_argument('--category', choices=['core', 'features', 'infrastructure', 'integration', 'all'], 
                       default='all', help='Test category to run')
    parser.add_argument('--test', help='Specific test file to run')
    
    args = parser.parse_args()
    
    test_dir = Path(__file__).parent
    
    # Test categories
    test_categories = {
        'core': [
            'test_commercial_solution.py',
            'test_tasi_correction.py', 
            'test_market_summary.py',
            'test_data_accuracy.py'
        ],
        'features': [
            'test_enhanced_theme.py',
            'test_css_separation.py'
        ],
        'infrastructure': [
            'test_db_loading.py',
            'test_module_loading.py'
        ],
        'integration': [
            'test_full_market.py',
            'test_optimization.py'
        ]
    }
    
    # Select tests to run
    if args.test:
        tests_to_run = [args.test]
    elif args.category == 'all':
        tests_to_run = []
        for category_tests in test_categories.values():
            tests_to_run.extend(category_tests)
    else:
        tests_to_run = test_categories.get(args.category, [])
    
    # Run tests
    print(f"🚀 SAUDI STOCK MARKET APP - TEST RUNNER")
    print(f"Category: {args.category}")
    print(f"Tests to run: {len(tests_to_run)}")
    
    passed = 0
    failed = 0
    
    for test_file in tests_to_run:
        test_path = test_dir / test_file
        if test_path.exists():
            if run_test_file(test_path):
                passed += 1
            else:
                failed += 1
        else:
            print(f"⚠️ Test file not found: {test_file}")
            failed += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"📊 TEST RESULTS")
    print(f"{'='*50}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%" if (passed+failed) > 0 else "No tests run")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
