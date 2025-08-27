# CSE API Tests

This directory contains test files for the CSE API functionality.

## Test Files

- `test_companies_subset.py` - Test getting companies for first 5 letters (A-E)
- `test_company_search.py` - Test company name search functionality
- `test_download.py` - Test updated download functionality
- `test_filtered_downloads.py` - Test filtered financial report downloads
- `test_quick.py` - Quick test for specific company's financial reports
- `test_updated_api.py` - Test updated API integration
- `run_tests.py` - Test runner script

## Running Tests

### Run All Tests

```bash
python tests/run_tests.py
```

### Run a Specific Test

```bash
python tests/run_tests.py test_quick
```

Or run directly:

```bash
python tests/test_quick.py
```

### Run from Tests Directory

```bash
cd tests
python run_tests.py
```

## Notes

- All test files automatically add the parent directory to the Python path to import the main modules (`app.py`, `download_financial_reports.py`, etc.)
- Tests may create files in the `reports/` directory
- Some tests may take time to complete as they make real API calls
- You can interrupt long-running tests with Ctrl+C
