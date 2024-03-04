"""
merge.py

Produce one CSV from all 30 CSVs from interval analysis.

Functions to merge data from multiple folders containing a JSON and and a CSV with metadata and scores over timestamps.
Overcome need to manually click through multiple folders by retrieving data automatically across many folders. Merge CSVs into one CSV with cumulatively adjusted timestamps.

Author: Anisha Iyer
"""

import pandas as pd
import numpy as np
import glob

def read_files(root, out_name):
    os.chdir(root)
    csv_files = glob.glob('*.csv')
    csv_files = sorted(list(csv_files))
    
    # only includes data csv files named based on starting second to ending second naming system
    # does not remerge finished csv with original data files if this is run twice
    csv_files = [f for f in csv_files if f[:1].isdigit()]
    print(csv_files)
    
    global data
    data = pd.DataFrame()

    i=0
    last_ts = 0
    last_frame = 0
    for f in csv_files:
        df = pd.read_csv(f)
        df, last_ts, last_frame = adjust_indices(df, last_ts, last_frame)
        df.insert(0, "Interval", len(df.index.values)*["Clip " + str(i+1) + ": " + str(f)][:3])
        data = pd.concat([data, df])
        i += 1
        
    data.index = pd.Index(range(len(data.index)))
    output = out_name + '.csv'
    data.to_csv(output)

def adjust_indices(df, ts, frame):
    df.loc[:, "Frame Index"] = df.loc[:, "Frame Index"].values + frame
    df.loc[:, "Timestamp(x)"] = df.loc[:, "Timestamp(x)"].values + ts
    return df, ts+30, frame+7200


# TODO: merge all of them but separate across before and after treatment

if __name__=="__main__":
    read_files(None)
    data