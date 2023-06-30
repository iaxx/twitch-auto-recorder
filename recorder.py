import requests
import os
import subprocess
import time
from dotenv import load_dotenv

# load env
load_dotenv()

def is_streamer_live(client_id, client_secret, username):
    # Get OAuth token
    response = requests.post(
        'https://id.twitch.tv/oauth2/token',
        params={
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }
    )

    oauth_token = response.json()['access_token']

    # Get streamer ID
    response = requests.get(
        f'https://api.twitch.tv/helix/users?login={username}',
        headers={'Client-ID': client_id, 'Authorization': f'Bearer {oauth_token}'}
    )

    user_id = response.json()['data'][0]['id']

    # Check if streamer is live
    response = requests.get(
        f'https://api.twitch.tv/helix/streams?user_id={user_id}',
        headers={'Client-ID': client_id, 'Authorization': f'Bearer {oauth_token}'}
    )

    data = response.json()['data']

    if data:
        print(f'{username} is live')
        return True
    else:
        print(f'{username} is not live')
        return False

def record_stream(client_id, client_secret, username, interval=300, filepath='G:\\RecordedLivestreams\\auto\\'): # Set your path here
    flag_file = None  # Moved outside the while loop so we can access it in the finally block

    try:
        while True:
            if is_streamer_live(client_id, client_secret, username):
                # Define the recording flag file path
                flag_file = os.path.join(filepath, f'{username}_recording')

                # If the flag file doesn't exist, then we start recording
                if not os.path.exists(flag_file):
                    filename = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
                    full_file_path = os.path.join(filepath, f'{filename}.mp4')

                    # Create the flag file
                    open(flag_file, 'a').close()

                    # Start the recording
                    command = f'streamlink -o {full_file_path} twitch.tv/{username} best'
                    subprocess.run(command, shell=True)

            time.sleep(interval)

    except KeyboardInterrupt:
        print('Interrupted by user')

    except Exception as e:
        print(f'Error occurred: {e}')

    finally:
        # Remove the flag file when script is terminated or an error occurs
        if flag_file and os.path.exists(flag_file):
            os.remove(flag_file)

client_id = os.getenv('TWITCH_CLIENT_ID', 'default_value')
client_secret = os.getenv('TWITCH_CLIENT_SECRET', 'default_value')
username = os.getenv('TWITCH_USERNAME', 'default_value')
record_stream(client_id, client_secret, username)
