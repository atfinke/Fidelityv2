# Fidelity v2

This includes two scripts:

- **fetcher.py**: Runs on a google cloud platform instance and downloads Fidelity portfolio data at the end of every weekday.
- **analyzer.py**: Loads data from downloaded fidelity csvs into a sqlite database.
