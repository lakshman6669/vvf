import os
import json
import re
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Define the root URL and endpoint for TikTok
tiktok_root = "https://www.ensembledata.com/apis"
tiktok_endpoint = "/tt/keyword/search"

# TikTok search route
@app.route('/', methods=['GET', 'POST'])
def tiktok_search():
    tiktok_data = []
    error_message = None

    if request.method == 'POST':
        keyword = request.form['keyword']

        # Define the parameters for the TikTok search API
        params = {
            "name": keyword,
            "cursor": 0,
            "period": 1,
            "sorting": 0,
            "country": "us",
            "match_exactly": False,
            "get_author_stats": False,
            "token": "wKVHqDaxzV9NwgBm"  # Make sure to use your actual token
        }

        try:
            # Make the API request
            res = requests.get(tiktok_root + tiktok_endpoint, params=params)
            res.raise_for_status()
            tiktok_raw_data = res.json()

            # Define the file path to save the raw JSON data locally
            raw_file_path = 'tiktok_search.json'

            # Write the raw data to tiktok_search.json file
            with open(raw_file_path, 'w') as json_file:
                json.dump(tiktok_raw_data, json_file, indent=4)

            print("Raw data has been successfully written to tiktok_search.json")

            # Extract and filter data from the JSON response
            input_string = str(tiktok_raw_data)  # Convert JSON data to string for regex processing

            # Define the new regular expression patterns for each field
            play_addr_url_pattern = r"'video':\s*\{\s*'play_addr':\s*\{\s*'uri':\s*'[^']+',\s*'url_list':\s*\[\s*'([^']+)"
            cover_url_pattern = r"'cover': \{'uri': '[^']*', 'url_list': \['(https?://[^\s]+)'\]"
            views_pattern = r"'play_count':\s*(\d+)"

            # Use re.findall to find all the matches for each field
            play_addr_url_matches = re.findall(play_addr_url_pattern, input_string)
            cover_url_matches = re.findall(cover_url_pattern, input_string)
            views_matches = re.findall(views_pattern, input_string)

            # Store the extracted data into a list of dictionaries
            for i in range(min(len(play_addr_url_matches), len(cover_url_matches), len(views_matches))):
                video_data = {
                    "play_addr_url": play_addr_url_matches[i],
                    "cover_url": cover_url_matches[i],
                    "views": views_matches[i]
                }
                tiktok_data.append(video_data)

            # Define the file path to save the filtered JSON data locally
            filtered_file_path = 'tiktok_extracted.json'

            # Write the filtered data to tiktok_extracted.json file
            with open(filtered_file_path, 'w') as json_file:
                json.dump(tiktok_data, json_file, indent=4)

            print("Filtered data has been successfully written to tiktok_extracted.json")

        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching data: {e}"
            print(error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)

    return render_template('indextiktok.html', tiktok_data=tiktok_data, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
