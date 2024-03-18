"""
sampling-rate.py

Single-use script to plot viable frame counts over each 30 second interval video clip.

Decided to log this in a spreadsheet. After logging this data, use this script to analyze and plot it.

Author: Anisha Iyer
"""
import pandas as pd

# manual viables information:
viables = {}

df = pd.read_csv("mouse_a_viables.csv")
print(df)

# fills up viables dictionary with keys of first rounded timepoint of that video's starting point
st = 0
for _ in range(30):
    viables[st] = []
    st += 30

