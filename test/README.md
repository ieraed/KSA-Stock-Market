# Saudi Stock Market App - Test Suite

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
