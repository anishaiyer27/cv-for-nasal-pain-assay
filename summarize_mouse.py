def check_total_grimace(mouse):
    print(mouse)
    
    full = (f+".csv")
    pre = (f+"_control.csv")
    post = (f+"_treated.csv")
    
    # full
    df = pd.read_csv(full)
    vals = df.loc[:, 'Total Grimace Score'].values
    new_df = df.dropna(subset=['Total Grimace Score'])
    non_nans = vals[~np.isnan(vals)]
    new_df.to_csv(mouse + '_full.csv')
    print("*** FULL ***")
    print("number of viable values for Total Grimace Score", len(non_nans))
    print("number of total values for Total Grimace Score", len(vals))
    print("average MGS score: ", np.mean(non_nans))
    print("median MGS score: ", np.median(non_nans))
    print("percent retained: ", str(100*len(non_nans)/len(vals)), "%\n")
    
    # pre
    df = pd.read_csv(pre)
    vals = df.loc[:, 'Total Grimace Score'].values
    new_df = df.dropna(subset=['Total Grimace Score'])
    non_nans = vals[~np.isnan(vals)]
    new_df.to_csv(mouse + '_pre_treatment.csv')
    print("*** PRE-TREAMTENT ***")
    print("number of viable values for Total Grimace Score", len(non_nans))
    print("number of total values for Total Grimace Score", len(vals))
    print("average MGS score: ", np.mean(non_nans))
    print("median MGS score: ", np.median(non_nans))
    print("percent retained: ", str(100*len(non_nans)/len(vals)), "%\n")
    
    
    # post
    df = pd.read_csv(post)
    vals = df.loc[:, 'Total Grimace Score'].values
    new_df = df.dropna(subset=['Total Grimace Score'])
    non_nans = vals[~np.isnan(vals)]
    new_df.to_csv(mouse + '_post_treatment.csv')
    
    print("*** POST-TREAMTENT ***")
    print("number of viable values for Total Grimace Score", len(non_nans))
    print("number of total values for Total Grimace Score", len(vals))
    print("average MGS score: ", np.mean(non_nans))
    print("median MGS score: ", np.median(non_nans))
    print("percent retained: ", str(100*len(non_nans)/len(vals)), "%\n")
    
# change for each mouse
mouse = "GX010160"
f = "results/" + mouse + "/" + mouse
check_total_grimace(f)