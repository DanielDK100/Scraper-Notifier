# -*- coding: utf-8 -*-
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class RefreshTokenHelper(object):
    @staticmethod
    def refresh():
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
            print('token.json exists')
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                print('Refreshes token')
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                credentials = flow.run_console()
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())
                print('Writes token to file')
