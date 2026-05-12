import os
import random

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file(
        'token.json',
        SCOPES
    )

if not creds or not creds.valid:

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            SCOPES
        )

        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

youtube = build('youtube', 'v3', credentials=creds)

videos = os.listdir('videos')

video_file = random.choice(videos)

video_path = f'videos/{video_file}'

titles = [
    'Relaxing Rain Sounds',
    'Deep Sleep Music',
    'Night Ambience',
    'Meditation Sounds'
]

title = random.choice(titles)

request = youtube.videos().insert(
    part='snippet,status',
    body={
        'snippet': {
            'title': title,
            'description': 'Automatic upload test',
            'tags': [
                'sleep',
                'relax',
                'rain',
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