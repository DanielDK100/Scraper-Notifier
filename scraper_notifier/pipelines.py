# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from ast import If, Try
import datetime
import os.path
from tkinter import E
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class ScraperNotifierPipeline(object):
    def process_item(self, item, spider):
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        creds = Credentials.from_authorized_user_file(os.path.dirname(os.path.abspath(__file__)) + '/token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        try:
            eventExist = service.events().get(calendarId='primary', eventId='vasketid' + item['reserved_at'].strftime('%Y%m%d%H%M')).execute()
        except:
            eventExist = None
        if eventExist is None:
            service.events().insert(calendarId='primary', body={
                'id': 'vasketid' + item['reserved_at'].strftime('%Y%m%d%H%M'),
                'summary': item['group'],
                'location': 'Degnestavnen, 2400 København NV',
                'start': {
                    'dateTime': item['reserved_at'].isoformat(),
                    'timeZone': 'Europe/Copenhagen',
                },
                'end': {
                    'dateTime': item['reserved_at'].isoformat(),
                    'timeZone': 'Europe/Copenhagen',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                        {'method': 'popup', 'minutes': 1440}
                    ],
                },
            }).execute()

        return item
