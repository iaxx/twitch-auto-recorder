# twitch-auto-recorder

A simple script that checks if a user is live every 5 minutes, it saves the video locally as an .mp4 and it avoids all ads. 

# Usage

1. Create an .env file in the folder with the script
2. Put in your Twitch API info and the user who's livestream you want to record.
3. Open recorder.py and on line 42 change the location where you want the video to be saved. 

-- Optionally --

Create a batch file with @echo off and run it with task scheduler in Windows to always have it running in the background .

# Dependencies 

Streamlink (not included)

# Known Issues

Sometimes the file that tracks if you're currently recording the livestream doesn't auto-delete.
