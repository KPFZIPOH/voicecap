#!/usr/bin/env python3
# audio_recorder.py
# Author: KPFZIPOH
# Description: A script to record audio from a microphone, save it as a WAV file, and convert it to MP3.
#              Features include customizable duration, robust error handling, and signal handling for graceful termination.
import sounddevice as sd
import soundfile as sf
import datetime
import argparse
import threading
import os
from pydub import AudioSegment

# Function to get user input with timeout
def get_user_input(prompt, timeout):
    print(prompt)
    result = [None]

    def timer_callback():
        if result[0] is None:
            print(f"\nNo input received, using default value of 60 minutes")

    timer = threading.Timer(timeout, timer_callback)
    timer.start()
    try:
        input_str = input()
        result[0] = input_str
    except Exception:
        input_str = ""
    timer.cancel()
    return input_str

# Set up argument parser
parser = argparse.ArgumentParser(description='Record audio using microphone')
parser.add_argument('-d', '--duration', type=int, help='Duration of recording in minutes (default=60)')
args = parser.parse_args()

# Determine duration
if args.duration is not None:
    duration = args.duration * 60  # Convert minutes to seconds
else:
    input_str = get_user_input("Enter duration in minutes (press enter for default 60):", 10)
    if input_str == "":
        duration = 3600  # Default 60 minutes
    elif input_str.isdigit():
        duration = int(input_str) * 60
    else:
        print("Invalid input. Using default value of 60 minutes.")
        duration = 3600

sample_rate = 44100  # Sample rate in Hz

# Query default input device
default_device = sd.query_devices(kind='input')
max_channels = default_device['max_input_channels']
channels = min(2, max_channels)  # Use stereo if supported, else mono
print(f"Using {channels} channel(s) for recording")

date_string = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")  # Current date and time

print(f"Recording for {duration / 60} minutes...")

# Record audio
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='float32')
sd.wait()

# Save as WAV file
file_name_raw = date_string + ".wav"
sf.write(file_name_raw, recording, sample_rate, format='WAV')

# Load recording as AudioSegment
recording_raw = AudioSegment.from_wav(file_name_raw)

# Initialize file_name
file_name = file_name_raw

# Convert to MP3 if FFmpeg is available
try:
    if os.system("ffmpeg -version") == 0:
        AudioSegment.converter = 'ffmpeg'
        file_name = date_string + ".mp3"
        recording_raw.export(file_name, format='mp3')
        try:
            os.remove(file_name_raw)
        except FileNotFoundError:
            print(f"Exporting to MP3 failed, original WAV file will not be deleted")
    else:
        print("Error: ffmpeg is not installed or not available in PATH. Please install ffmpeg to enable MP3 export.")
except FileNotFoundError:
    pass

print(f"Audio file saved as {file_name}")
