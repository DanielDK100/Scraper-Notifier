# -*- coding: utf-8 -*-
import subprocess


class MailHelper(object):
    @staticmethod
    def send_postfix_mail(body, subject, sender='admin@danielwinther.dk', recipient='danielwinther@hotmail.dk'):
        subprocess.call('echo "' + body + '" | mail -s "' +
                        subject + '" -a "From: Notifikation <' + sender + '>" ' + recipient, shell=True)
