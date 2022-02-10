# -*- encoding:utf-8 -*-
# author: liuheng
import json
from flask import Flask, g
from storages.redis import RedisClient
from setting import GENERATOR_MAP
from loguru import logger

__all__ = ['app']

app = Flask(__name__)

account = 'account'
credential = 'credential'

@app.route('/')
def index():
    return '<h2>Welcome to Account Pool System</h2>'

def get_conn():
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, f'{website}_{credential}', RedisClient(credential, website))
            setattr(g, f'{website}_{account}', RedisClient(account, website))

        return g

@app.route('/<website>/random')
def random(website):
    g = get_conn()
    getattr(g, f'{website}_{account}').set(username, password)
    return json.dumps({'status': '1'})

@app.route('/<website>/count')
def count(website):
    """
    get count of credential
    """
    g = get_conn()
    count = getattr(g, f'{website}_{credential}').count()
    return json.dumps({'status': 'ok', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
