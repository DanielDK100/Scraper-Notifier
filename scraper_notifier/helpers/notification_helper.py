# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from models import ReservationDB, db_connect, create_table
from scraper_notifier.helpers.mail_helper import MailHelper


class NotificationHelper(object):
    @staticmethod
    def run_notifications():
        engine = db_connect()
        create_table(engine)
        Session = sessionmaker(bind=engine)

        session = Session()
        reservations = session.query(ReservationDB).filter(
            ReservationDB.notified_at == None).filter(
            ReservationDB.reserved_at <= datetime.now() - timedelta(hours=1)).all()
        for reservation in reservations:
            reservation.notified_at = datetime.now()
            MailHelper.send_postfix_mail('Husk reservation af vaskemaskine d. ' +
                                         reservation.reserved_at.strftime('%d/%m-%Y %H:%M') + ' maskine ' + reservation.group + '', 'Reservation af vaskemaskine d. ' + reservation.reserved_at.strftime('%d/%m-%Y %H:%M'))
        try:
            session.commit()
            print('Notfications was run succesfully')
        except:
            session.rollback()
            raise
        finally:
            session.close()
