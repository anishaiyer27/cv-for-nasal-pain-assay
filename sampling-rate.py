"""
sampling-rate.py

Single-use script to plot viable frame counts over each 30 second interval video clip.

Decided to log this in a spreadsheet. After logging this data, use this script to analyze and plot it.

Author: Anisha Iyer
"""

# manual viables information:
viables = {}

# fills up viables dictionary with keys of first rounded timepoint of that video's starting point
st = 0
for _ in range(30):
    viables[st] = []
    st += 30


# TODO: finish for the rest of them
viables[0] = [9] # barely
# 30 - 60:
viables[30] = [11, 24, 25]

# 60 - 90: 19 ears only, 21 1 ear only, 
viables[60] = [0, 2, 3, 4, 5, 6, 13, 14, 15, 16, 19, 21, 22, 23, 26]

print(viables)