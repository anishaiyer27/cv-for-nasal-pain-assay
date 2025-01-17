"""
merge.py

Produce one CSV from all 30 CSVs from interval analysis.

Functions to merge data from multiple folders containing a JSON and and a CSV with metadata and scores over timestamps.
Overcome need to manually click through multiple folders by retrieving data automatically across many folders. Merge CSVs into one CSV with cumulatively adjusted timestamps.

Author: Anisha Iyer
"""

import pandas as pd
import numpy as np
import glob, os, argparse, sys

def read_files(root, mouse):
    os.chdir(root)
    csv_files = glob.glob('*'+mouse+'*.csv')

    all_starts = []

    for f in csv_files:
        splits = f.split("anishaiyer_")
        if len(splits)==1:
            if "anishaiyer2" in f:
                splits = f.split("anishaiyer2_")
            else:
                splits = f.split("anishaiyer3_")
        new_name = int(splits[1][:7].split("-")[0])
        all_starts.append(new_name)
    
    encode = {i:st for st,i in list(enumerate(all_starts))}
    all_starts = sorted(list(all_starts))
    order = [encode[st] for st in all_starts]
    ordered_files = [csv_files[o] for o in order]
    
    # only includes data csv files named based on starting second to ending second naming system
    # does not remerge finished csv with original data files if this is run twice
    csv_files = [f for f in csv_files if f[:1].isdigit()]
    global data
    data = pd.DataFrame()

    i=0
    last_ts = 0
    last_frame = 0
    expected_length = 0
    for f in ordered_files:
        df = pd.read_csv(f)
        print("read ", f, " as csv")
        df, last_ts, last_frame = adjust_indices(df, last_ts, last_frame)
        expected_length += len(df.index.values)
        df.insert(0, "Interval", len(df.index.values)*["Clip " + str(i+1) + ": " + str(f)][:3])
        data = pd.concat([data, df])
        i += 1
    
    data.index = pd.Index(range(len(data.index)))
    print("expected length", expected_length)
    print("actual length", len(data.index.values))

def adjust_indices(df, ts, frame):
    df.loc[:, "Frame Index"] = df.loc[:, "Frame Index"].values + frame
    df.loc[:, "Timestamp(x)"] = df.loc[:, "Timestamp(x)"].values + ts
    return df, ts+30, frame+7200

def save_full_csv(root, mouse):
    os.chdir(root)
    output = mouse + '.csv'
    data.to_csv(output)

def read_from_csv(root, mouse, st, click):
    csv = root+"/"+mouse+".csv"
    global data
    data = pd.read_csv(csv)
    save_ctrl_vs_treated(root, mouse, st, click)

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
    parser.add_argument("csv", help="Whether to read from CSV or data stream", type=str)
    parser.add_argument("mouse_out", help="End time of pre-treatment section. Time in seconds when mouse is removed", type=int)
    parser.add_argument("mouse_return", help="Start of post-treatment section at time of click of chamber lid. Time in seconds when mouse is removed", type=int)
    args = parser.parse_args()

    if_csv = (args.csv == "True")

    if not if_csv:
        data_dir = cwd + '/data' + '/' + args.mouseID
        print(data_dir)
        read_files(data_dir, args.mouseID)
        print("completed")
        save_full_csv(cwd, args.mouseID)
        save_ctrl_vs_treated(cwd, args.mouseID, args.mouse_out, args.mouse_return)
    else:
        data_dir = cwd + '/results' + '/' + args.mouseID
        read_from_csv(data_dir, args.mouseID, args.mouse_out, args.mouse_return)