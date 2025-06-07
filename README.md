# Disclaimer
The author is not responsible for any misuse of this software. Use it at your own risk and ensure compliance with all applicable laws and regulations.

# Ethical Considerations
Use Responsibly: This software is for educational and testing purposes only. Using a keylogger to monitor someone without their explicit consent is illegal in many jurisdictions and violates privacy rights.

Transparency: Always inform and obtain consent from users before deploying this software on their systems.

Security: The ZIP file is encrypted, but ensure the password and output files are handled securely to prevent unauthorized access.

# voicecap
This app would allow you to record the sound of the computer without being noticed.  Due to the file size could possibly generated, it runs one hour by default, if you would like to capture the voice continuously,  you could use windows task scheduler to run it on hourly basis.
# Audio Recorder

**Author**: KPFZIPOH
**Description**: A Python script to record audio from a microphone, save it as a WAV file, and convert it to MP3 format. The script supports customizable recording durations, command-line arguments, and graceful termination handling.

Note: This project is intended for educational purposes only. Unauthorized use of voicecap to capture mic/voice of remote computer without consent is illegal and unethical. Ensure you have explicit permission from all parties involved before using this software.

## Features
- Record audio for a specified duration (default: 60 minutes).
- Save recordings as MP3 files, with temporary WAV files automatically deleted upon successful conversion.
- Support for command-line arguments to set duration and output directory.
- Interactive prompt for duration with a timeout (defaults to 60 minutes if no input is provided).
- Graceful handling of termination signals (e.g., Ctrl+C).
- Automatic creation of an output directory for storing audio files.
- Robust error handling for recording, file saving, and MP3 conversion.

## Requirements
- **Python 3.6+**
- **Dependencies**:
  - `sounddevice`: For audio recording.
  - `soundfile`: For saving audio as WAV files.
  - `pydub`: For converting WAV to MP3.
- **FFmpeg**: Required for MP3 conversion. Install it separately (see installation instructions below).  you need to put the ffmpeg.exe to the same folder as voicecap.exe

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/audio-recorder.git
   cd audio-recorder
