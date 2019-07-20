import os

# Waiting for google to authenticate
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from secret import Secrets

# Used for temporary function to get videos from youtube
import urllib3
from bs4 import BeautifulSoup


class YouTubeApi:
    getSecret = Secrets()
    key = getSecret.youtube()

    @staticmethod
    def scoob():
        return "Not working :("

    # Still needs to be authorised
    def test(self):
        scopes = ['https://www.googleapis.com/auth/youtube.readonly']
        api_service_name = 'youtube'
        api_version = 'v3'
        client_secrets_file = 'YOUR_CLIENT_SECRET_FILE.json'

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=self.key
        )
        response = request.execute()

        print(response)
