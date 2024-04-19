"""
merge.py

Produce one CSV from all 30 CSVs from interval analysis.

Functions to merge data from multiple folders containing a JSON and and a CSV with metadata and scores over timestamps.
Overcome need to manually click through multiple folders by retrieving data automatically across many folders. Merge CSVs into one CSV with cumulatively adjusted timestamps.

Author: Anisha Iyer
"""

import pandas as pd
import numpy as np
import glob, os, argparse

def read_files(root, mouse):
    os.chdir(root)
    csv_files = glob.glob('*'+mouse+'.csv')
    csv_files = sorted(list(csv_files))
    
    # only includes data csv files named based on starting second to ending second naming system
    # does not remerge finished csv with original data files if this is run twice
    csv_files = [f for f in csv_files if f[:1].isdigit()]
    
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

def adjust_indices(df, ts, frame):
    df.loc[:, "Frame Index"] = df.loc[:, "Frame Index"].values + frame
    df.loc[:, "Timestamp(x)"] = df.loc[:, "Timestamp(x)"].values + ts
    return df, ts+30, frame+7200

def save_full_csv(root, mouse):
    os.chdir(root)
    output = mouse + '.csv'
    data.to_csv(output)


# merge all of them but separate across before and after treatment given timestamps for split
    
def save_ctrl_vs_treated(root, mouse, st, click):
    os.chdir(root)
    before = mouse + '_control.csv'
    after = mouse + '_treated.csv'
    st = float(str(st).zfill(3))
    click = float(str(click).zfill(3))
    ctrl = data.loc[data["Timestamp(x)"] <= st] # split across before and after
    treated = data.loc[data["Timestamp(x)"] >= click]
    ctrl.to_csv(before)
    treated.to_csv(after)


# merge all of them but separate across before and after treatment given vid # and frame #s

def save_ctrl_vs_treated2(root, mouse, vid1, frame_st, vid2, frame_click):
    """
        Alternate helper method which reads in user friendly inputs. Get index numbers
        and starting times of filenames from PainFace.
    """
    os.chdir(root)
    before = mouse + '_control.csv'
    after = mouse + '_treated.csv'
    #vid1 = 
    ctrl = data.loc[data["Frame Index"] <= frame_st+vid1*240] # split across before and after
    treated = data.loc[data["Frame Index"] >= frame_click+vid2*240]
    ctrl.to_csv(before)
    treated.to_csv(after)
    # method is untested
    return NotImplementedError

if __name__=="__main__":
    cwd = os.getcwd()
    print(cwd)

    parser = argparse.ArgumentParser("merging script")
    parser.add_argument("mouseID", help="ID associated with mouse", type=str)
    parser.add_argument("mouse_out", help="End time of pre-treatment section. Time in seconds when mouse is removed", type=int)
    parser.add_argument("mouse_return", help="Start of post-treatment section at time of click of chamber lid. Time in seconds when mouse is removed", type=int)
    args = parser.parse_args()
    read_files(cwd, args.mouseID)
    save_full_csv(cwd, args.mouseID)
    save_ctrl_vs_treated(cwd, args.mouseID, args.mouse_out, args.mouse_return)
    data