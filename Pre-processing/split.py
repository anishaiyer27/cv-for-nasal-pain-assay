"""
split.py

Simple script that reads in a mouse behavior video in MP4 format and produces several resultant videos each in 30 second segments.
Author: Anisha Iyer
"""

# TODO: install a JDK

from moviepy.editor import VideoFileClip

filename = "midterm2review.mp4" # hardcoded filename with current behavior video file (temporarily)
file_loc = "/Users/anishaiyer/Downloads/" # hardcoded filepath

video = VideoFileClip(file_loc+filename)
## get duration of video in seconds via:
duration = video.duration

segment_duration = 30

num_segments = int(duration // segment_duration)
print(duration, num_segments)

for i in range(num_segments):
    start_time = i * segment_duration
    end_time = min((i+1)* segment_duration, duration)

    subclip = video.subclip(start_time, end_time)

    subclip.write_videofile(f"{file_loc}{start_time}-{end_time}_{filename}.mp4", codec="libx264")


video.close()


"""
# length of video in seconds
length = ffmpeg.probe(file_loc + filename)["format"]["duration"]
print("length of video: ", length)

times = [i*30 for i in range(num_segments)]

for t in times:
    ffmpeg_extract_subclip(filename, t, t+30, targetname=str(t, "-", t+30, "_", filename)+".mp4")
"""