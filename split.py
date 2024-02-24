"""
split.py

Simple script that reads in a mouse behavior video in MP4 format and produces several resultant videos each in 30 second segments.
Author: Anisha Iyer
"""

# TODO: install a JDK

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

filename = "MOUSE_A.MP4" # hardcoded filename with current behavior video file (temporarily)
file_loc = "Documents/Anisha/"

## get duration of video in seconds via:

# length of video in seconds
length = ffmpeg.probe(file_loc + filename)["format"]["duration"]
print("length of video: ", length)
num_segments = length // 30
times = [i*30 for i in range(num_segments)]

for t in times:
    ffmpeg_extract_subclip(filename, t, t+30, targetname=str(t, "-", t+30, "_", filename)+".mp4")
