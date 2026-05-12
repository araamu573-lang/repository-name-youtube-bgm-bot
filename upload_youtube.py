import random
import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',
    SCOPES
)

creds = flow.run_local_server(port=0)

youtube = build('youtube', 'v3', credentials=creds)

videos = os.listdir('videos')

video_file = random.choice(videos)

video_path = f'videos/{video_file}'

titles = [
    'Relaxing Rain Sounds for Sleep',
    'Deep Sleep Ambient Music',
    'Peaceful Night Rain Ambience',
    'Calming Meditation Music'
]

title = random.choice(titles)

request = youtube.videos().insert(
    part='snippet,status',
    body={
        'snippet': {
            'title': title,
            'description': 'Daily relaxing ambient video.',
            'tags': [
                'sleep music',
                'rain sounds',
                'relax',
                'meditation'
            ],
            'categoryId': '10'
        },
        'status': {
            'privacyStatus': 'public'
        }
    },
    media_body=MediaFileUpload(video_path)
)

response = request.execute()

print(response)