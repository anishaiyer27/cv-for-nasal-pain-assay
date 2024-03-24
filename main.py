from analyze import *
from merge import *
from sampling_rate import sampling_rate as sr


# make more user friendly by reading in args (eventually)
# find a user friendly way to indicate viable frames after visual inspection if combining all csvs into 1 csv
data = pd.read_csv("MOUSE_A.csv")

# retrieve dict of facial action unit keys and viable frame values
viables = sr.execute()
print(sr.faus)

# exploratory data analysis
eda(data, viables)

# get high confidence scores per fau, corresponding timestamps, and overall sorted clean data matrix
f,t,s = get_all_fau_scores()
display_analytics_report(f,t,s)

# eventually change the structure of this to only query results for what figures the user wants to create