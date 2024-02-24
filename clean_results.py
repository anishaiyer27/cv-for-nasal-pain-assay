"""
clean_results.py

Data cleaning from multiple folders containing a JSON and and a CSV with metadata and scores over timestamps.
Overcome need to manually click through multiple folders by retrieving data automatically across many folders.

Read in information from user about which frames were classified with accurate bounding boxes. 

Author: Anisha Iyer
"""

import pandas as pd

# TODO: make more streamlineable
data = pd.read_csv("30-60.csv")

data.head()

fau_names = data.columns[3:7]
conf_names = data.columns[10:14]

# have user input viable indices where bounding boxes are accurate
viables = [11, 24, 25]
faus = data.loc[viables, fau_names]