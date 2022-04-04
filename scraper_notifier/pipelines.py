# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from ast import If, Try
import os.path
from tkinter import E
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class AddCalendarEvent(object):
    def process_item(self, item, spider):
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        creds = Credentials.from_authorized_user_file(os.path.dirname(os.path.abspath(__file__)) + '/token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        service.events().import_(calendarId='primary', body={
            'iCalUID': item['type'] + item['event_at'].strftime('%Y%m%d%H%M'),
            'summary': item['summary'],
            'location': item['location'],
            'start': {
                'dateTime': item['event_at'].isoformat(),
                'timeZone': 'Europe/Copenhagen',
            },
            'end': {
                'dateTime': item['event_at'].isoformat(),
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
