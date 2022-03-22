# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from scraper_notifier.models import ReservationDB, db_connect, create_table


class ScraperNotifierPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        reservationExists = session.query(ReservationDB).filter(
            ReservationDB.reserved_at == item['reserved_at']).filter(
            ReservationDB.group == item['group']).first()

        if reservationExists is None:
            reservation_item = ReservationDB()
            reservation_item.reserved_at = item['reserved_at']
            reservation_item.group = item['group']
            reservation_item.ordered_at = item['ordered_at']

            try:
                session.add(reservation_item)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item
