# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import timedelta
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class AddCalendarEvent(object):
    def process_item(self, item, spider):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        TIME_ZONE = 'Europe/Copenhagen'

        credentials = Credentials.from_authorized_user_file(os.path.dirname(os.path.abspath(__file__)) + '/token.json', SCOPES)
        service = build('calendar', 'v3', credentials=credentials)

        service.events().import_(calendarId='primary', body={
            'iCalUID': item['type'] + item['event_at'].strftime('%Y%m%d%H%M'),
            'summary': item['summary'],
            'description': item['description'],
            'start': { 'dateTime': item['event_at'].isoformat(), 'timeZone': TIME_ZONE },
            'end': { 'dateTime': (item['event_at'] + timedelta(hours=2)).isoformat(), 'timeZone': TIME_ZONE },
            'location': item['location'],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 30},
                    {'method': 'popup', 'minutes': 1440}
                ],
            },
        }).execute()

        return item
