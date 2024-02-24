"""
analyze.py

Analyze data from multiple folders containing a JSON and and a CSV with metadata and scores over timestamps.
Overcome need to manually click through multiple folders by retrieving data automatically across many folders.

Read in information from user about which frames were classified with accurate bounding boxes. 

For now, this script will read in one CSV file and one JSON to produce one averaged MGS score for 1 30 second interval.
Later, this functionality will move to clean_results.py and will work across multiple folders.

Author: Anisha Iyer
"""

import pandas as pd

# TODO: get all CSVs from all folders, start with prototype code for 1 CSV




pd.read_csv("Downloads/2024-02-22_anishaiyer_30-60 mouse a bt.mp4_5124cba9-4d32-4cc8-84af-92e607ccdd54")