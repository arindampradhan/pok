#!/usr/bin/env python  ##########################################################
# -*- coding: utf-8 -*-                                                         #
#                                                                               #
# Inspired from https://github.com/dadrc/pocket-cli/blob/master/pocket-cli.py   #
#################################################################################

import requests
import ConfigParser
from os.path import isfile, expanduser
from sys import exit
from const import *


def getCode(key):
    """
    Get code by giving consumer_key and redirect_uri.
    """
    PAYLOAD = {
        'consumer_key': key,
        'redirect_uri': REDIRECT_URI
    }
    r = requests.post(OAUTH_URL, data=PAYLOAD, verify=False)
    code = str(r.text).split("=")[1]
    message = ("\033[93m\033[1mPlease open..\033[0m\n"  # authorizing from user
               "https://getpocket.com/auth/authorize?request_token={0}"
               "&redirect_uri=https://getpocket.com/connected_accounts"
               "\n\n\033[93m\033[1mAuthorize the app in your browser!\033[0m"
               "  \033[93m\033[1mYou can use poc after that easily...\033[0m")
    print message.format(code)
    return code


def writeConfig(code="", token=""):
    """
    Write to .pocketrc
    """
    try:
        config.add_section('OAUTH')
    except:
        pass
    if code:
        config.set('OAUTH', 'code', code)
    if token:
        config.set('OAUTH', 'token', token)
    with open(rc_file, 'w+') as f:
        config.write(f)


def getConfig():
    """
    Read from .pocketrc
    """
    config.read(rc_file)
    # print "config:", config
    try:
        code = config.get('OAUTH', 'code')
    except:
        code = ''
    try:
        token = config.get('OAUTH', 'token')
        token = token.split("&username")[0]
    except:
        token = ''
    return code, token


def getAccessToken(key, code):
    """
    Get the access token after you get the code.
    """
    PAYLOAD = {
        'consumer_key': key,
        'code': code
    }
    r = requests.post(OAUTH_AUTH_URL, data=PAYLOAD, verify=False)
    token = str(r.text).split("=")[1]
    token = token.split("&username")[0]
    return token


def authenticate(key=key):
    """
    Authentication handler function
    1st create config file.         | .pocketrc
    2st getCode @ oauth/request     | OAUTH_URL
    3rd User authorizes the app     | message
    4th getAccess @ oauth/authorize | OAUTH_AUTH_URL
    """
    if not isfile(rc_file):
        print u"\033[93m\033[1mCreating your config file!\033[0m"
        writeConfig()
    # get code and token if present else ''
    code, token = getConfig()
    # no token, no code, start oauth
    if ((token == None or token == '') and code == ''):
        code = getCode(key)
        writeConfig(code=code)                             # store in .pocketrc
        exit()
    # got code, get token
    elif ((token == None or token == '') and code != ''):
        token = getAccessToken(key, code)
        # print token
        if not token:
            print u"\033[93m\033[1mCool you have authorized the app! \033[0m\033[93m\U0001F44D\033[0m"
        # store in .pocketrc
        writeConfig(code=code, token=token)

    return {'code': code, 'token': token}
