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
import signal
import sys
from pydub import AudioSegment

# Global flag to handle recording termination
recording_stopped = False

def signal_handler(sig, frame):
    """Handle termination signals (e.g., Ctrl+C) to stop recording gracefully."""
    global recording_stopped
    print("\nTermination signal received. Stopping recording...")
    recording_stopped = True
    sd.stop()  # Stop the recording process
    sys.exit(0)

def get_user_input(prompt, timeout, default_duration=60):
    """
    Get user input with a timeout, returning the default duration if no input is provided.
    
    Args:
        prompt (str): The prompt to display to the user.
        timeout (int): Timeout duration in seconds.
        default_duration (int): Default recording duration in minutes.
    
    Returns:
        int: Duration in seconds.
    """
    print(prompt)
    timer = threading.Timer(timeout, print, args=[f"\nNo input received, using default value of {default_duration} minutes"])
    timer.start()
    try:
        input_str = input()
        timer.cancel()
        if input_str.strip():
            try:
                duration = int(input_str)
                if duration <= 0:
                    raise ValueError("Duration must be positive")
                return duration * 60
            except ValueError as e:
                print(f"Invalid input: {e}. Using default duration of {default_duration} minutes.")
                return default_duration * 60
        return default_duration * 60
    except KeyboardInterrupt:
        timer.cancel()
        print(f"\nInput interrupted, using default value of {default_duration} minutes")
        return default_duration * 60

def ensure_output_directory(directory="recordings"):
    """
    Ensure the output directory exists, creating it if necessary.
    
    Args:
        directory (str): The directory to store audio files.
    
    Returns:
        str: Path to the output directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def main():
    """Main function to handle audio recording, saving, and conversion."""
    # Set up signal handlers for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Set up argument parser for command-line options
    parser = argparse.ArgumentParser(description="Record audio using a microphone and save as MP3.")
    parser.add_argument(
        '-d', '--duration',
        type=int,
        help='Duration of recording in minutes (default=60)',
        default=None
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='recordings',
        help='Directory to store output audio files (default=recordings)'
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Determine recording duration
    default_duration = 60  # Default duration in minutes
    if args.duration is not None:
        if args.duration <= 0:
            print("Error: Duration must be a positive integer. Using default duration.")
            duration = default_duration * 60
        else:
            duration = args.duration * 60
    else:
        duration = get_user_input(
            f"Enter recording duration in minutes, press Enter for default ({default_duration}): ",
            timeout=10,
            default_duration=default_duration
        )

    # Audio recording parameters
    sample_rate = 44100  # Sample rate in Hz
    channels = 2         # Stereo audio
    date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Timestamp for file naming

    # Ensure output directory exists
    output_dir = ensure_output_directory(args.output_dir)
    file_name_raw = os.path.join(output_dir, f"{date_string}.wav")
    file_name_mp3 = os.path.join(output_dir, f"{date_string}.mp3")

    print(f"Starting recording for {duration / 60:.1f} minutes...")

    try:
        # Record audio
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
        
        # Wait until recording finishes or is interrupted
        sd.wait()

        if recording_stopped:
            print("Recording stopped early due to termination signal.")
            return

        # Save recording as WAV file
        sf.write(file_name_raw, recording, sample_rate, format='WAV')
        print(f"Saved temporary WAV file: {file_name_raw}")

        # Convert WAV to MP3
        try:
            AudioSegment.converter = 'ffmpeg'  # Ensure ffmpeg is used for conversion
            recording_raw = AudioSegment.from_wav(file_name_raw)
            recording_raw.export(file_name_mp3, format='mp3', bitrate='192k')
            print(f"Audio file converted and saved as: {file_name_mp3}")

            # Remove temporary WAV file
            try:
                os.remove(file_name_raw)
                print(f"Temporary WAV file deleted: {file_name_raw}")
            except FileNotFoundError:
                print("Warning: Temporary WAV file not found for deletion.")
        except FileNotFoundError as e:
            print(f"Error: FFmpeg not found. Please ensure FFmpeg is installed. Keeping WAV file: {file_name_raw}")
        except Exception as e:
            print(f"Error during MP3 conversion: {e}. Keeping WAV file: {file_name_raw}")

    except Exception as e:
        print(f"Error during recording: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
