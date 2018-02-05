# -*- coding: utf-8 -*-

import requests


def acccess(http_info):
    request_info = http_info
    if 'payload' not in http_info:
        request_info['payload'] = {}
    if 'headers' not in http_info:
        request_info['headers'] = {}
    if 'querystring' not in http_info:
        request_info['querystring'] = {}

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


def main(user, pass_):
    res = acccess({
        'method': 'GET',
        'url': 'http://127.0.0.1:8000/admin',
    })
    cookie = res.cookies['csrftoken']

    res = acccess({
        'method': 'POST',
        'url': 'http://127.0.0.1:8000/ja/admin/login/',
        'querystring': {'next': '/ja/admin'},
        'payload': 'username={}&password={}&this_is_the_login_form=1&mezzanine_login_interface=admin&csrfmiddlewaretoken={}'.format(user, pass_, cookie),
        'headers': {
            'cookie': 'csrftoken={}'.format(cookie),
            'referer': 'http://127.0.0.1:8000/',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'http://127.0.0.1:8000',
            'cache-control': 'no-cache',
            'postman-token': '65f3c7af-fb2a-553d-f697-bc31821e69ef'
        },
    })
    print(res.text)


if __name__ == '__main__':
    main("tom", "tom")
