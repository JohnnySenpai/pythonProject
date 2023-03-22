import requests
import youtube_dl

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set the URL for the Twitch API
API_URL = "https://api.twitch.tv/helix/clips"

client_id = '4dgfyhrm9xzxa6okj4lx3mc8t09txp'

client_secret = '2jjnz0hbcd1nn1injicsy46vqlol7c'

auth_url = 'https://id.twitch.tv/oauth2/token'

headers = {
    "Client-ID": client_id  # Replace with your own client ID
}

payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
}

response = requests.post(auth_url, headers=headers, data=payload)


access_token = response.json()['access_token']

params = {
    "game_id": "33214",  # The game ID for Apex Legends
    "first": 1,  # The number of clips to retrieve per request (max 100)
    # "sort": "views",  # Sort the results by number of views
}

headers = {
    "Client-ID": client_id,  # Replace with your own client ID
    "Accept": "application/vnd.twitchtv.v5+json",
    'Authorization': 'Bearer ' + access_token
}

# Make the API request
response = requests.get(API_URL, params=params, headers=headers)

# Check the response status code

if response.status_code != 200:
    print("There was an error with the request")
    exit()

# Get the data from the response
data = response.json()


# Get the URL for the clip
url = data["data"][0]['url']

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])



# Save the video data to the specified file path
# with open("C:/Users/Gjon Vila/Desktop/most_viewed_clip.mp4", "wb") as file:
#     file.write(response.content)
#     file.close()

# Set the credentials for your Google account
creds = Credentials.from_authorized_user_info({
    "access_token": "YOUR_ACCESS_TOKEN",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "token_uri": "https://oauth2.googleapis.com/token"
})

# Set the parameters for the video file you want to upload
file_path = "PATH_TO_YOUR_VIDEO_FILE"
video_title = "YOUR_VIDEO_TITLE"
video_description = "YOUR_VIDEO_DESCRIPTION"
video_tags = ["TAG1", "TAG2", "TAG3"]

# Create a YouTube Shorts client
service = build("youtube", "v1", credentials=creds)

try:
    request = service.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": video_title,
                "description": video_description,
                "tags": video_tags
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=file_path
    )
    response = request.execute()
    print(f"Uploaded video: {response['id']}")
except HttpError as error:
    print(f"An error occurred while uploading the video: {error}")
# Use the YouTube Shorts client to upload the video file
