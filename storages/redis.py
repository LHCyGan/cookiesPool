# -*- encoding:utf-8 -*-
# author: liuheng
import random
import redis
from setting import *


class RedisClient:
    """
    redis 客户端
    """

    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_HOST, password=REDIS_PASSWORD):
        """
        初始化redis客户端
        :param type: 存储的内容类型
        :param website: 网站名称
        :param host: 主机
        :param port: 端口
        :param password:密码
        """
        self.db = redis.StrictRedis(host==host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        拼接type 和 website 组成hash结构
        :return:
        """
        return f'{self.type}:{self.website}'

    def get(self, username):
        return self.db.hget(self.name(), username)

    def delete(self, username):
        return self.db.hdel(self.name(), username)

    def count(self):
        return self.db.hlen(self.name())

    def random(self):
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        return self.db.keys(self.name())

    def all(self):
        return self.db.hgetall(self.name())