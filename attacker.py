# -*- coding: utf-8 -*-

import requests


def main():
    url = "http://127.0.0.1:8000/admin"
    res = requests.get(url)
    # print(res.text)
    # for c in res.cookies:
    #     print(c.name, c.value)
    print(res.cookies["csrftoken"])


if __name__ == '__main__':
    main()
