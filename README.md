# MAI201 Assignment 2: Data Validation and Testing

Data validation on a messy customer dataset using Great Expectations, plus pytest unit tests for three utility functions.

## Files

- `setup_expectations.py` — defines and saves the Great Expectations suite (8 expectations)
- `run_validation.py` — runs the suite against `data/customer_data.csv` and generates the HTML report
- `src/utils.py` — the three functions under test: `load_csv`, `clean_phone`, `validate_email`
- `tests/test_utils.py` — 16 pytest unit tests covering those functions
- `conftest.py` — lets pytest resolve the `src` package on import
- `data/customer_data.csv` — the dataset being validated
- `assignment2_report.md` — written report with findings, screenshots, and reflection
- `screenshots/` — validation results and pytest output

## How to run

```bash
pip install great-expectations pytest pandas

python setup_expectations.py
python run_validation.py
pytest tests/ -v
```

## Results

All eight expectations failed against the real data, each pointing to a genuine issue: out-of-range ages, invalid countries, duplicate and missing customer IDs, malformed emails, missing salary values, and invalid signup dates. Full counts are in `assignment2_report.md`. All 16 pytest tests pass.
