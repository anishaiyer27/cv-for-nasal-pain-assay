from analyze import *
from merge import *


# make more user friendly by reading in args (eventually)
# find a user friendly way to indicate viable frames after visual inspection if combining all csvs into 1 csv
data = pd.read_csv("30-60.csv")

# exploratory data analysis
eda(data)

# get high confidence scores per fau, corresponding timestamps, and overall sorted clean data matrix
f,t,s = get_clean_fau_analytics()
display_analytics_report(f,t,s)

# eventually change the structure of this to only query results for what figures the user wants to create