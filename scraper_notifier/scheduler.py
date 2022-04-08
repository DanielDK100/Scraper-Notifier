# -*- coding: utf-8 -*-
import time
import os
from scraper_notifier.helpers.refresh_token_helper import RefreshTokenHelper
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta

scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Copenhagen', 'apscheduler.job_defaults.max_instances': '10'})
scheduler.start()
print('------------------------------------------------------------')
print('Scheduler initialized\n')
two_minutes = timedelta(minutes=2).total_seconds()
start_date = '2020-01-01 00:00:00'

scheduler.add_job(RefreshTokenHelper.refresh, 'interval', hours=24, start_date=start_date, id='refresh_token')
scheduler.add_job(os.system, 'interval', hours=3, jitter=two_minutes, start_date=start_date, id='laundry', args=['scrapy crawl laundry'])

print('Scheduled jobs:')
for job in scheduler.get_jobs():
    print(job.id + ': ' + str(job.next_run_time))
print('------------------------------------------------------------')
while True:
    time.sleep(1)
