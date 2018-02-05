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
