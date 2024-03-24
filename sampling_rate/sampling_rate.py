"""
sampling-rate.py

Single-use script to plot viable frame counts over each 30 second interval video clip.

Decided to log this in a spreadsheet. After logging this data, use this script to analyze and plot it.

Author: Anisha Iyer
"""

import pandas as pd
import matplotlib.pyplot as plt


csv = pd.read_csv("sampling-rate/mouse_a_viables.csv")
global faus
faus = ['Orbital 1', 'Orbital 2', 'Nose', 'Whiskers', 'Ear 1', 'Ear 2']

def clean_viables(csv):
    csv.columns = csv.loc[4]
    csv = csv.drop(list(range(5)))
    csv.index = pd.Index(range(len(csv.index)))
    csv = csv.drop(columns=['Clip number'])
    return csv

def to_dict(csv, fau_names=faus):
    arrs = dict(csv)
    for k in fau_names:
        arrs[k] = dict(arrs[k].dropna())
        for i in arrs[k].keys():
            vals = arrs[k][i].split(',')
            #temp = []
            #for v in vals:
                #if v.isdigit():
                    #temp.append(int(v))
            vals = [int(v) for v in vals]
            arrs[k][i] = vals
    return arrs

def execute():
    clean = clean_viables(csv)
    arrs = to_dict(clean)
    yeet = arrs.keys() - faus
    yeet.remove('Viable indices')
    [arrs.pop(key) for key in yeet]
    return arrs

def plot_accurate_boxes(args):
    """
    Plot accuracies for bounding box classifications for each facial action unit.
    """
    
    arrs = execute()

    for f in faus:
        d = arrs[f]
        counts = [len(v) for v in d.values()]
        plt.title(f)
        plt.xlim(0, 15)
        plt.ylim(0, 30)
        plt.bar(d.keys(), counts)
        plt.show()
        plt.savefig(f+'.png')