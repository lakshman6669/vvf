import os
import json
import re
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Define the root URL and endpoint
root = "https://ensembledata.com/apis"
endpoint = "/youtube/search"

@app.route('/', methods=['GET', 'POST'])
def index():
    videos_data = []
    error_message = None

    if request.method == 'POST':
        keyword = request.form['keyword']

        # Define the parameters for the YouTube search API
        params = {
            "keyword": keyword,
            "depth": 1,
            "start_cursor": "",
            "period": "overall",
            "sorting": "relevance",
            "get_additional_info": False,
            "token": "wKVHqDaxzV9NwgBm"
        }

        try:
            # Make the API request
            res = requests.get(root + endpoint, params=params)
            res.raise_for_status()
            youtube_data = res.json()

            # Define the file path to save the raw JSON data locally
            raw_file_path = 'C:/Users/uppal/OneDrive/Desktop/Original/youtube_search.json'

            # Create the directory if it doesn't exist
            raw_directory = os.path.dirname(raw_file_path)
            os.makedirs(raw_directory, exist_ok=True)

            # Write the raw data to youtube_search.json file
            with open(raw_file_path, 'w') as json_file:
                json.dump(youtube_data, json_file, indent=4)

            print("Raw data has been successfully written to youtube_search.json")

            # Extract and filter data from the JSON response
            input_string = str(youtube_data)  # Convert JSON data to string for regex processing

            # Define the new regular expression patterns for each field
            video_id_pattern = r"'videoRenderer': \{'videoId': '([^']*)'"
            title_pattern = r"'title': \{'runs': \[\{'text': '([^']*)'"
            channel_pattern = r"'longBylineText': \{'runs': \[\{'text': '([^']*)'"
            views_pattern = r"'viewCountText': \{'simpleText': '([^']*) views'"
            published_time_pattern = r"'publishedTimeText': \{'simpleText': '([^']*)'"
            thumbnail_url_pattern = r"'thumbnail': \{'thumbnails': \[\{'url': '([^']*)'"

            # Use re.findall to find all the matches for each field
            video_id_matches = re.findall(video_id_pattern, input_string)
            title_matches = re.findall(title_pattern, input_string)
            channel_matches = re.findall(channel_pattern, input_string)
            views_matches = re.findall(views_pattern, input_string)
            published_time_matches = re.findall(published_time_pattern, input_string)
            thumbnail_url_matches = re.findall(thumbnail_url_pattern, input_string)

            # Check if there are any matches
            if not video_id_matches:
                print("No video IDs found")

            if not title_matches:
                print("No titles found")

            if not channel_matches:
                print("No channels found")

            if not views_matches:
                print("No view counts found")

            if not published_time_matches:
                print("No published times found")

            if not thumbnail_url_matches:
                print("No thumbnail URLs found")

            # Store the extracted data into a list of dictionaries
            for i in range(min(len(video_id_matches), len(title_matches), len(channel_matches), len(views_matches), len(published_time_matches), len(thumbnail_url_matches))):
                video_data = {
                    "video_id": video_id_matches[i],
                    "title": title_matches[i],
                    "channel": channel_matches[i],
                    "views": views_matches[i],
                    "published_time": published_time_matches[i],
                    "thumbnail_url": thumbnail_url_matches[i]
                }
                videos_data.append(video_data)

            # Define the file path to save the filtered JSON data locally
            filtered_file_path = 'C:/Users/uppal/OneDrive/Desktop/Original/youtube_extracted.json'

            # Write the filtered data to youtube_extracted.json file
            with open(filtered_file_path, 'w') as json_file:
                json.dump(videos_data, json_file, indent=4)

            print("Filtered data has been successfully written to youtube_extracted.json")

        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching data: {e}"
            print(error_message)  # Debug print statement
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)  # Debug print statement

    return render_template('indexyoutube.html', videos_data=videos_data, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
