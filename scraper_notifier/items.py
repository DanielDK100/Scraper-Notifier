# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags


class EventItem(scrapy.Item):
    type = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    summary = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    event_at = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    location = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
