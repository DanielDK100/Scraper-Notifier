# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy_splash import SplashRequest
from scrapy.utils.response import open_in_browser
from scrapy.loader import ItemLoader
from cryptography.fernet import Fernet
from dateutil import parser
from scraper_notifier.helpers.login_helper import LoginHelper
from ..items import EventItem


class LaundrySpider(scrapy.Spider):
    name = 'laundry'
    base_url = 'http://80.71.140.62/'
    login_url = base_url + 'aLog.asp'
    start_urls = [
        base_url + 'SoegReservation.asp?VisSlettede=0'
    ]

    key = LoginHelper.get_encryptionKey()
    login_information = LoginHelper.get_login_information('laundry')
    username = key.decrypt(login_information['username'])
    password = key.decrypt(login_information['password'])

    def start_requests(self):
        yield scrapy.Request(self.login_url, self.parse_login, meta={'proxy': None})

    def parse_login(self, response):
        return FormRequest.from_response(response, formdata={
            'username': self.username, 'password': self.password}, callback=self.start_crawl, meta={'proxy': None})

    def start_crawl(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={'proxy': None})

    def parse(self, response):
        table = response.css('table:last-of-type')
        for reservation in table.css('tr')[1:]:
            reserved_at = reservation.css(
                'td > font:nth-of-type(1)::text').get().strip() + ' ' + reservation.css(
                'td:nth-of-type(2)::text').get().strip().replace('kl. ', '')
            ordered_at = reservation.css(
                'td:nth-of-type(4)::text').get().strip()

            loader = ItemLoader(item=EventItem(), selector=reservation)
            loader.add_value('type', 'lau')
            loader.add_value('location', 'Degnestavnen, 2400 København NV')
            loader.add_value('event_at', parser.parse(reserved_at, dayfirst=True))
            loader.add_css('summary', 'td:nth-of-type(3)::text')

            yield loader.load_item()
