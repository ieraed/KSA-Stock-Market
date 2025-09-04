#!/usr/bin/env python3
"""
Test Organization Script for Saudi Stock Market App
Organizes all test files into a single 'test' directory and removes obsolete files.
"""

import os
import shutil
from pathlib import Path

def organize_tests():
    """Organize all test files into a unified test directory"""
    
    # Base directory
    base_dir = Path("C:/Users/raed1/OneDrive/Saudi Stock Market App")
    test_dir = base_dir / "test"
    
    print("🧹 ORGANIZING TESTS INTO UNIFIED DIRECTORY")
    print("=" * 50)
    
    # Create test directory if it doesn't exist
    test_dir.mkdir(exist_ok=True)
    
    # Essential tests to keep (organized by category)
    essential_tests = {
        # Core functionality tests
        "test_commercial_solution.py": "Commercial solution validation",
        "test_tasi_correction.py": "TASI price correction system",
        "test_market_summary.py": "Market summary functionality",
        "test_data_accuracy.py": "Data accuracy validation",
        
        # Feature-specific tests
        "test_enhanced_theme.py": "Theme customization features",
        "test_css_separation.py": "CSS separation functionality",
        
        # Database and loading tests
        "test_db_loading.py": "Database loading functionality",
        "test_module_loading.py": "Module loading and imports",
        
        # Integration tests
        "test_full_market.py": "Full market integration test",
        "test_optimization.py": "Performance optimization tests"
    }
    
    # Test files to remove (obsolete/duplicate)
    obsolete_tests = [
        "test_complete_fixes.py",          # Replaced by commercial solution
        "test_ranking_fix.py",             # Merged into market summary
        "test_market_fix.py",              # Duplicate of market_fixes
        "test_market_fixes.py",            # Consolidated into market_summary
        "test_specific_stocks.py",         # Covered by commercial solution
        "test_thimar_debug.py",            # Specific debugging, no longer needed
        "test_thimar_tamkeen.py",          # Covered by commercial solution
        "test_symbol_mapping.py",          # Basic functionality, covered elsewhere
        "test_database_debug.py",          # Debugging file, not a proper test
        "test_enhanced_summary.py",        # Merged into market_summary
        "test_ultra_fast_complete.py",    # Covered by optimization tests
        "test_market_data.py"              # Duplicate of data_accuracy
    ]
    
    # Debug files to remove (no longer needed)
    debug_files = [
        "debug_db.py",
        "debug_market_summary.py", 
        "debug_market_value.py",
        "debug_missing_stocks.py",
        "debug_parsing.py",
        "debug_value_movers.py",
        "minimal_test.py",
        "quick_test.py",
        "simple_test.py"
    ]
    
    # Temporary test files to remove
    temp_files = [
        "final_price_fix_demo.py",
        "comprehensive_optimization_test.py",
        "critical_issue_resolver.py",
        "quick_optimization_test.py",
        "quick_tasi_test.py",
        "performance_debug.py",
        "price_accuracy_analysis.py"
    ]
    
    moved_count = 0
    removed_count = 0
    
    # Move essential tests to test directory
    print("\n📂 MOVING ESSENTIAL TESTS:")
    for test_file, description in essential_tests.items():
        source_path = base_dir / test_file
        target_path = test_dir / test_file
        
        if source_path.exists():
            try:
                shutil.move(str(source_path), str(target_path))
                print(f"  ✅ {test_file} → test/ ({description})")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Failed to move {test_file}: {e}")
        else:
            print(f"  ⚠️ {test_file} not found")
    
    # Remove obsolete test files
    print("\n🗑️ REMOVING OBSOLETE TESTS:")
    for test_file in obsolete_tests:
        file_path = base_dir / test_file
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"  ✅ Removed {test_file}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {test_file}: {e}")
        else:
            print(f"  ⚠️ {test_file} not found")
    
    # Remove debug files
    print("\n🔧 REMOVING DEBUG FILES:")
    for debug_file in debug_files:
        file_path = base_dir / debug_file
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"  ✅ Removed {debug_file}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {debug_file}: {e}")
        else:
            print(f"  ⚠️ {debug_file} not found")
    
    # Remove temporary files
    print("\n🧹 REMOVING TEMPORARY FILES:")
    for temp_file in temp_files:
        file_path = base_dir / temp_file
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"  ✅ Removed {temp_file}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {temp_file}: {e}")
        else:
            print(f"  ⚠️ {temp_file} not found")
    
    # Move existing testing directory content
    existing_testing_dir = base_dir / "testing"
    if existing_testing_dir.exists():
        print("\n📁 MERGING EXISTING TESTING DIRECTORY:")
        for file in existing_testing_dir.iterdir():
            if file.is_file() and file.suffix == '.py':
                target_path = test_dir / file.name
                try:
                    shutil.move(str(file), str(target_path))
                    print(f"  ✅ {file.name} → test/")
                    moved_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to move {file.name}: {e}")
        
        # Remove empty testing directory
        try:
            existing_testing_dir.rmdir()
            print(f"  ✅ Removed empty testing/ directory")
        except Exception as e:
            print(f"  ⚠️ Could not remove testing/ directory: {e}")
    
    # Create test index file
    print("\n📋 CREATING TEST INDEX:")
    create_test_index(test_dir, essential_tests)
    
    # Create test runner
    print("🏃 CREATING TEST RUNNER:")
    create_test_runner(test_dir)
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ TEST ORGANIZATION COMPLETE!")
    print(f"📂 Moved {moved_count} essential tests to test/ directory")
    print(f"🗑️ Removed {removed_count} obsolete/debug files")
    print(f"📁 All tests now organized in: {test_dir}")
    print("\nTo run tests: python test/run_tests.py")
    
    return test_dir

def create_test_index(test_dir, essential_tests):
    """Create an index file documenting all tests"""
    index_file = test_dir / "README.md"
    
    content = """# Saudi Stock Market App - Test Suite

## Overview
This directory contains all tests for the Saudi Stock Market Trading Signals App.

## Test Categories

### Core Functionality Tests
- `test_commercial_solution.py` - Commercial solution validation (main integration test)
- `test_tasi_correction.py` - TASI price correction system
- `test_market_summary.py` - Market summary functionality
- `test_data_accuracy.py` - Data accuracy validation

### Feature-Specific Tests
- `test_enhanced_theme.py` - Theme customization features
- `test_css_separation.py` - CSS separation functionality

### Infrastructure Tests
- `test_db_loading.py` - Database loading functionality
- `test_module_loading.py` - Module loading and imports

### Integration Tests
- `test_full_market.py` - Full market integration test
- `test_optimization.py` - Performance optimization tests

### Legacy Tests
- `tasi_comparison_test.py` - TASI comparison (from testing/ directory)

## Running Tests

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test
```bash
python test_commercial_solution.py
```

### Run by Category
```bash
python run_tests.py --category core
python run_tests.py --category features
python run_tests.py --category integration
```

## Test Guidelines

1. **Commercial Solution Test** - Main integration test that validates the complete system
2. **TASI Correction Test** - Validates price accuracy against official TASI data
3. **Market Summary Test** - Ensures market data is processed correctly
4. **Data Accuracy Test** - Validates data fetching and processing accuracy

## Notes

- All tests use live data from Saudi Exchange
- Tests are designed to work with the commercial-ready solution
- No hardcoded test data or symbols (fully dynamic)
- Tests validate both performance and accuracy requirements
"""
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Created test/README.md")

def create_test_runner(test_dir):
    """Create a unified test runner script"""
    runner_file = test_dir / "run_tests.py"
    
    content = '''#!/usr/bin/env python3
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
        print(f"\\n{'='*50}")
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
    print(f"\\n{'='*50}")
    print(f"📊 TEST RESULTS")
    print(f"{'='*50}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%" if (passed+failed) > 0 else "No tests run")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open(runner_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Created test/run_tests.py")

if __name__ == "__main__":
    organize_tests()
