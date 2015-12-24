#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
from os.path import isfile, expanduser

import logging
logging.captureWarnings(True)

DEFAULT_COUNT = 20                 # set it acc. to ur needs
key = "49474-c946e877614e2e6794f360e4"

# constants for poc.py
BASE_URL = "https://getpocket.com/v3/"
GET_URL = BASE_URL + "get"
ADD_URL = BASE_URL + "add"
DELETE_URL = BASE_URL + "send"

C1 = u"\033[1m\u25D8 %s\033[0m"    # Title color
C3 = u"\033[93m\033[1m%s \033[0m"  # Link color
C2 = u"\033[93m└\u25E6 %s \033[0m" # Warning color
C4 = u"\033[93m %s \033[0m"        # Warning color
C5 = u'\033[47m\033[30m%s\033[0m'  # Tag color

HEADERS = {'content-type': 'application/json'}
PAYLOAD = {
    "consumer_key": key,
    "access_token": "not given!",
}


# constants for auth.py
BASE_URL = "https://getpocket.com/v3/"
OAUTH_URL = BASE_URL + "oauth/request"
OAUTH_AUTH_URL = BASE_URL + "oauth/authorize"
REDIRECT_URI = 'https://getpocket.com/connected_accounts'


rc_file = expanduser('~/.pocketrc')
config = ConfigParser.RawConfigParser(allow_no_value=True)
token = ""
