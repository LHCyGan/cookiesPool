# -*- encoding:utf-8 -*-
# author: liuheng
import json
import requests
from requests.exceptions import ConnectionError
from storages.redis import *
from exceptions.init import InitException
from loguru import logger


class BaseTester:

    def __init__(self, website=None):
        self.website = website
        if not self.website:
            raise InitException
        self.account_operator = RedisClient(type='account', website=self.website)
        self.credential_operator = RedisClient(type='credential', website=self.website)

    def test(self, username, credential):
        raise NotImplementedError

    def run(self):
        credentials = self.credential_operator.all()
        for username, credential in credentials.items():
            self.test(username, credential)

class Antispider6Tester(BaseTester):
    def __init__(self):
        super(Antispider6Tester, self).__init__()

    def test(self, username, credential):
        logger.info(f'testing credential for {username}')
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, headers={'Cookie': credential},\
                                    timeout=5, allow_redirects=False)
            if response.status_code == 200:
                logger.info('test failed')

        except ConnectionError:
            logger.info('test failed')



class Antispider7Tester(BaseTester):
    """
    tester for antispider7
    """

    def __init__(self, website=None):
        BaseTester.__init__(self, website)

    def test(self, username, credential):
        """
        test single credential
        """
        logger.info(f'testing credential for {username}')
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, headers={
                'authorization': f'jwt {credential}'
            }, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                logger.info('credential is valid')
            else:
                logger.info('credential is not valid, delete it')
                self.credential_operator.delete(username)
        except ConnectionError:
            logger.info('test failed')