# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
from cryptography.fernet import Fernet


class LoginHelper(object):
    settings = get_project_settings()

    @staticmethod
    def get_login_information(login):
        loginInformation = LoginHelper.settings.get('LOGINS')[login]
        return loginInformation

    @staticmethod
    def get_encryptionKey():
        key = Fernet(LoginHelper.settings.get('ENCRYPTION_KEY'))
        return key
