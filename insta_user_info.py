from flask import Flask, render_template, request
import requests
import json
import os
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    filtered_data = []

    if request.method == 'POST':
        username = request.form['username']
        root = "https://www.ensembledata.com/apis"
        user_info_endpoint = "/instagram/user/info"
        reels_endpoint = "/instagram/user/reels"

        params = {
            "username": username,
            "token": "wKVHqDaxzV9NwgBm"
        }

        try:
            res = requests.get(root + user_info_endpoint, params=params)
            res.raise_for_status()
            user_info = res.json()
            print(f"User Info: {user_info}")  # Debug print statement

            if 'data' in user_info and 'pk_id' in user_info['data']:
                pk_id = user_info['data']['pk_id']
                reels_params = {
                    "user_id": pk_id,
                    "depth": 1,
                    "include_feed_video": True,
                    "oldest_timestamp": 1666262030,
                    "start_cursor": "",
                    "chunk_size": "10",
                    "token": "wKVHqDaxzV9NwgBm"
                }

                reels_res = requests.get(root + reels_endpoint, params=reels_params)
                reels_res.raise_for_status()
                reels_data = reels_res.json()
                print(f"Reels Data: {reels_data}")  # Debug print statement

                # Check if reels_data is not empty
                if reels_data:
                    # Define the file path to save the JSON file locally
                    file_path = 'C:/Users/uppal/OneDrive/Desktop/Original/reels_data.json'

                    # Create the directory if it doesn't exist
                    directory = os.path.dirname(file_path)
                    os.makedirs(directory, exist_ok=True)

                    # Write the data to reels_data.json file
                    with open(file_path, 'w') as json_file:
                        json.dump(reels_data, json_file, indent=4)

                    print("Data has been successfully written to reels_data.json")

                    # Filter the data from reels_data.json
                    filtered_data = filter_reels_data(file_path)

                else:
                    error_message = "No reels data found for this user."
            else:
                error_message = "pk_id not found in user info response."
        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching data: {e}"
            print(error_message)  # Debug print statement
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)  # Debug print statement

    return render_template('indexinsta.html', error_message=error_message, filtered_data=filtered_data)

def filter_reels_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            input_string = json_file.read()

        # Define the regular expression pattern for video data
        video_data_pattern = r'"video_versions":\s*\[\s*\{[^}]*"url":\s*"([^"]+\.mp4[^"]*)"'

        # Define the regular expression pattern for like counts
        like_data_pattern = r'"like_count":\s*(\d+)'

        # Use re.findall to find all the URLs
        video_matches = re.findall(video_data_pattern, input_string)

        # Use re.findall to find all the like counts
        like_matches = re.findall(like_data_pattern, input_string)

        # Check if there are any matches
        if not video_matches:
            print("No video URLs found")

        if not like_matches:
            print("No like counts found")

        filtered_data = []
        # Print the video URLs and like counts together
        for i in range(min(len(video_matches), len(like_matches))):
            video_url = video_matches[i]
            like_count = like_matches[i]
            filtered_data.append({'video_url': video_url, 'like_count': like_count})
            print(f"{{video_url: {video_url}, like_count: {like_count}}}")

        return filtered_data

    except Exception as e:
        print(f"An error occurred while filtering reels data: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True)
