import pandas as pd
import numpy as np

"""
analyze.py

Reads in information from user about which frames were classified with accurate bounding boxes. 

For now, this script will read in one CSV file and one JSON to produce one averaged MGS score for 1 30 second interval.
Later, this functionality will move to clean_results.py and will work across multiple folders.

Author: Anisha Iyer
"""

#data = pd.read_csv("30-60.csv")

# TODO: make more streamlineable
def eda(dataset, viables):
    """
        Prints first five rows of data matrix. Processes arguments.
        Cleans data matrix for only MGS scores and confidences for user-specified frames only.

        Parameters:
            - "data_arg": list containing frame indices of interest
                - switch to trad args object
        
        Allocates:
            - global "data": stores data in global "data" variable
            - global "clean_data": cleans data and stores lean dataset in global "clean_data" variable
                - contains only MGS scores for each FAU and Confidences for each FAU score
                - columns 3-7 and 10-14 from full dataset ("data")
    """
    global data
    data = dataset
    print("First five rows of PainFace CSV: \n", data.head())

    # EXPLORATORY DATA ANALYSIS:
    global FAU_NAMES
    print(data.columns, "\n\n\n")
    FAU_NAMES = data.columns[5:9]
    print(FAU_NAMES, "\n\n\n")

    global CONF_NAMES
    CONF_NAMES = data.columns[12:16]
    print(CONF_NAMES, "\n\n\n")

    # have user input viable indices where bounding boxes are accurate
    data_arg = [11, 24, 25]
    # helper function to get viables
    set_clean_data(viables, type=1)
    print("\n\n\nCLEAN DATA:\n\n\n", clean_data)
    

def set_clean_data(viables, type=1):
    """
        Helper function to clean dataframe of rows with poorly classified bounding boxes or other
        foundational inaccuracies. Processes viable dict argument and selects only for specified
        frames.

        Sets global clean_data variable.
    """
    global clean_data
    clean_data = pd.DataFrame()
    if not type: # if existing viable indices list provides final lists of viable indices for each clip 
        inner = viables['Viable indices']
        temp = []
        for clip in inner.keys():
            frames = inner[clip]
            adder = [clip*30]*len(frames)
            temp.extend(adder + frames)
        viables_lst = temp

        faus = data.loc[viables_lst, FAU_NAMES]
        fau_arr = np.asarray(faus)
        confs = data.loc[viables_lst, CONF_NAMES]
        conf_arr = np.asarray(confs)

        clean_data = faus.join(confs)
    elif type==1:
        clean_viable_dict = {}
        minF = 100000
        maxF = -1
        for fau in FAU_NAMES:
            print('fau: ',fau)
            print('\n\n\nviables keys:', viables.keys())
            scnd_index = [v for v in viables.keys() if fau in v][-1]
            inner = viables[scnd_index]
            clean_viable_dict[fau] = []
            for clip in inner.keys():
                frames = inner[clip]
                frames = [clip*30 + f for f in frames]
                clean_viable_dict[fau].extend(frames)
            minF = min(clean_viable_dict.values())[0]
            maxF = max([v[-1] for v in clean_viable_dict.values()])
        
        #max_length = max([len(clean_viable_dict[fau]) for fau in FAU_NAMES])
        print(minF, ", ", maxF)
        domain = list(range(minF, maxF+1))
        print("domain: ", domain)

        columns = list(FAU_NAMES)
        columns.extend(CONF_NAMES)

        print(data.columns, "alsdkjflkdj")
        
        for c in columns:
            if columns.index(c) < len(columns)//2:
                this_fau = c
            else:
                print("\n\n",columns.index(c))
                this_fau = list(data.columns)[columns.index(c)]
            print("c: ", c, " this fau: ", this_fau)

            print("does clean_data exist yet?")
            
            if clean_data.empty:
                clean_data = data.loc[domain, c].to_frame()
            else:
                clean_data.join(data.loc[domain, c])
            print("now yes")
            print(domain)
            print("remove: ", clean_viable_dict[this_fau])
            # for each fau, make the non-viable values null and also make corresponding confs null
            nulls = list(domain)
            print("nulls:", nulls)
            for f in clean_viable_dict[this_fau]:
                #print(f)
                nulls.remove(f)
            print(list(clean_data.axes))
            clean_data.loc[nulls, c] = np.nan
            print(clean_data)
        
        #for c in range(len(CONF_NAMES)):
        #    clean_data.join(data.loc[clean_viable_dict[FAU_NAMES[c], CONF_NAMES[c]]])
    pd.save_csv('MOUSE_A_clean.csv')


def viables_by_confidence():
    """
        Sorts clean dataset by Get clean data per FAU after filtering for high confidence scores only.
        
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
        
        # data for this FAU where confidence of FAU score >= threshold
        mgs = clean_data[fau].where(clean_data[conf] >= THRESHOLD).dropna()
        # sort in order of greatest confidence (high confidence to low confidence)
        mgs_sorted = clean_data.sort_values(conf, ascending=False)[fau]
        sorted_arrs = np.asarray(mgs_sorted)
        faus[fau] = np.asarray(mgs)
        times[fau] = mgs.index
        fs_sorted[fau] = sorted_arrs
    
    return faus, times, fs_sorted

def get_all_fau_scores(): 
    """
        Get data per FAU without filtering for manually confirmed bounding box accuracy.
        Run the same analytics as with clean data on all timestamps of the data matrix without checking
        whether the bounding boxes were correctly identified at those points.

        Returns:
            - "faus": dictionary of MGS scores for each FAU after filtering for high confidence scores only
            - "times": corresponding times in the video for each datapoint in FAUs values
            - "fs_sorted": same as FAUs except in order of confidence (high to low) and without dropping low confidence scores
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
    """
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
    """
    return NotImplemented

def get_clean_rows(temp, show_all_confidences=False):
    """
        For each frame, computes average confidence over all FAU scores. Adds a column for average confidence values
        and sorts data from high average confidence to low average confidence.

        Parameters:
            - "temp": any dataframe, doesn't need to be global data variable (can pass in full dataset or clean_data with viables only)

        Returns:
            - "filtered": 

            
        Original Description:
            Get clean data per row after filtering for high confidence rows only.
            Filter for rows that correspond to high average confidence value across Facial Action Units.
            Returns a dictionary with viable FAU scores at timepoints of accurate bounding box classification and high confidence scores across facial action units.

        Filtering not implemented in this function
    """
    THRESHOLD = 0.90
    
    # insert new column with average confidence value
    if "Avg Confidence" in temp.columns.values:
        temp = temp.drop(columns=['Avg Confidence'])
    temp.insert(len(temp.columns), "Avg Confidence", np.mean(np.asarray(temp.loc[:, CONF_NAMES]), axis=1))

    # this sorts by average confidence, but doesn't filter by anything or remove any rows
    filtered = temp.sort_values(by='Avg Confidence', ascending=False)
    fau = filtered.loc[:, FAU_NAMES]
    conf = filtered.loc[:, CONF_NAMES]
    avg = filtered.loc[:, 'Avg Confidence']
    filtered = fau.join(avg)

    # join confidence columns back as well
    if show_all_confidences:
        filtered = fau.join(avg).join(conf)
    
    return filtered
    
# get_clean_rows(data)
