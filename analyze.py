import pandas as pd
import numpy as np

"""
analyze.py

Reads in information from user about which frames were classified with accurate bounding boxes. 

For now, this script will read in one CSV file and one JSON to produce one averaged MGS score for 1 30 second interval.
Later, this functionality will move to clean_results.py and will work across multiple folders.

Author: Anisha Iyer
"""

# TODO: get all CSVs from all folders, start with prototype code for 1 CSV
#data = pd.read_csv("30-60.csv")

# TODO: make more streamlineable
def eda(data_arg):
    global data
    data = data_arg
    print(data.head())

    # EXPLORATORY DATA ANALYSIS:
    global FAU_NAMES
    FAU_NAMES = data.columns[3:7]

    global CONF_NAMES
    CONF_NAMES = data.columns[10:14]

    # have user input viable indices where bounding boxes are accurate
    data_arg = [11, 24, 25]
    viables = viables
    faus = data.loc[viables, FAU_NAMES]
    fau_arr = np.asarray(faus)
    confs = data.loc[viables, CONF_NAMES]
    conf_arr = np.asarray(confs)

    global clean_data
    clean_data = faus.join(confs)
    print("lean data matrix: ", clean_data)

def get_all_fau_scores(data):
    """
        Get data per FAU without filtering for manually confirmed bounding box accuracy.
        Run the same analytics as with clean data on all timestamps of the data matrix without checking
        whether the bounding boxes were correctly identified at those points.
    """
    
    THRESHOLD = 0.90
    
    faus = {}
    fs_sorted = {}
    times = {}
    
    for i in range(len(FAU_NAMES)):
        fau = FAU_NAMES[i]
        conf = CONF_NAMES[i]
        
        mgs = data[fau].where(data[conf] >= THRESHOLD).dropna()
        mgs_sorted = data.sort_values(conf, ascending=False)[fau]
        sorted_arrs = np.asarray(mgs_sorted)
        print(mgs)
        #print(mgs_sorted, "\n")
        faus[fau] = np.asarray(mgs)
        print("index", mgs.index, "\n")
        times[fau] = mgs.index
        fs_sorted[fau] = sorted_arrs
    
    return faus, times, fs_sorted

def get_clean_fau_analytics():
    """
        Get clean data per FAU after filtering for high confidence scores only.
        
        For each Facial Action Unit, filter for datapoints that correspond to high confidence values.
        
        Returns 3 dictionaries with:
            - Faus: data arrays with all high confidence scores organized by FAU identity
            - Times: label arrays containing timestamp identity for each included confidence score per FAU
            - Scores sorted: dataframes containing all FAU scores sorted by confidence across each individual column
    """
    THRESHOLD = 0.90
    
    faus = {}
    fs_sorted = {}
    times = {}
    
    for i in range(len(FAU_NAMES)):
        fau = FAU_NAMES[i]
        conf = CONF_NAMES[i]
        
        mgs = clean_data[fau].where(clean_data[conf] >= THRESHOLD).dropna()
        mgs_sorted = clean_data.sort_values(conf, ascending=False)[fau]
        sorted_arrs = np.asarray(mgs_sorted)
        faus[fau] = np.asarray(mgs)
        times[fau] = mgs.index
        fs_sorted[fau] = sorted_arrs
    
    return faus, times, fs_sorted

def display_analytics_report(faus, times, fs_sorted):
    # user friendly report:
    
    tstamps = {}
    [tstamps.update({k:np.asarray(data.loc[times[k], "Timestamp(x)"])}) for k in times.keys()]
    
    print("\n\n\n*** COMPLETED FAU ANALYTICS ON CLEAN DATAFRAME ***\n\n")
    
    for fau in faus.keys():
        print("\n\n**", fau, "**\n\n")
        print("For", fau, "Facial Action Unit:\n")
        print("High confidence Mouse Grimace Scale scores for this clip:\n", faus[fau])
        print("\nCorresponding timestamps for high confidence MGS score:\n", tstamps[fau])
        print("\nAll viable Mouse Grimace Scale scores descending order of Confidence Score:\n", fs_sorted[fau])
    

def get_fau_scores(viables, fau, conf):
    """
        Get arrays of Facial Action Unit scores across each row of data that has been determined to be viable through visual inspection.
        IGNORE. not pursuing this anymore.
    """
    THRESHOLD = 0.90
    
    fau_mgs = {}
    for fau in FAU_NAMES:
        fau_mgs[str(fau)] = []
    
    for v in range(len(viables)):
        for fi in range(len(fau)):
            if conf[v][fi] >= THRESHOLD:
                pass
                #print(fau_mgs[list(fau_mgs.keys())[fi]], fau[v][fi])
                #fau_mgs[list(fau_mgs.keys())[fi]].append(fau[v][fi])
    
    print(fau_mgs)
    return NotImplemented

def get_clean_rows(temp):
    """
        Get clean data per row after filtering for high confidence rows only.
        
        Filter for rows that correspond to high average confidence value across Facial Action Units.
        Returns a dictionary with viable FAU scores at timepoints of accurate bounding box classification and high confidence scores across facial action units.
    """
    THRESHOLD = 0.90
    
    # insert new column with average confidence value
    if "Avg Confidence" in temp.columns.values:
        temp = temp.drop(columns=['Avg Confidence'])
    temp.insert(len(temp.columns), "Avg Confidence", np.mean(np.asarray(temp.loc[:, CONF_NAMES]), axis=1))
    filtered = temp.sort_values(by='Avg Confidence', ascending=False)
    fau = filtered.loc[:, FAU_NAMES]
    conf = filtered.loc[:, CONF_NAMES]
    avg = filtered.loc[:, 'Avg Confidence']
    filtered = fau.join(avg)
    # join confidence columns as well
    #filtered = fau.join(avg).join(conf)
    
    return filtered