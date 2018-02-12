# Requests Attacker

## Overview

Password list attack to mezzanine admin page for internal test by using requests

## Requirement

- python3
- pip3
- git

## Usage

- basic usage

```
(requests_attacker) kazu0716 $ python attacker.py
User: aaa, Pass: bbbb, Result: Failed
User: vvv, Pass: aaa, Result: Failed
User: aaaa, Pass: aaaa, Result: Failed
User: aaa, Pass: aaa, Result: Failed
User: tom, Pass: tom, Result: Succeeded
```

- attcker config file

```
(requests_attacker) kazu0716 MacBook-Pro-4 $ cat attacker.conf
[general]
# access url
url=http://127.0.0.1:8000/ja/admin/login/

[http_headers]
# useragent = random
useragent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
referer=http://127.0.0.1:8000/
accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept_language=ja,en-us;q=0.7,en;q=0.3

[interval]
# access interval by using sleep from min to max
# min and max are XX sec 
max=3
min=1
```

- modify user_id and password

```
(requests_attacker) kazu0716 MacBook-Pro-4 $ cat attack_list.csv
user,password
aaa,bbbb
vvv,aaa
aaaa,aaaa
aaa,aaa
tom,tom
```

## Install

```
git clone https://github.com/kazu0716/requests_attacker.git
cd ./requests_attacker
pip3 install -r requirement.txt
python3 attacker.py
```
