#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""


        ███████████████████████████████████
        ███████████████████████████████████
        ███████▀███████████████████▀███████
        ████████▄▀███████████████▀▄████████
        ██████████▄▀███████████▀▄██████████
         ███████████▄▀███████▀▄███████████
          ████████████▄▀███▀▄████████████
           █████████████▄ ▄█████████████
            ███████████████████████████
              ███████████████████████
                 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

Need help, issue a request:
@ https://github.com/arindampradhan/pok/issues

Usage:
  pok (ls   | list)   [COUNT]
  pok (sh   | search) <NAME>
  pok (t    | tag)    <NAME>
  pok (fav  | favourite)
  pok (unr  | unread)
  pok (arcv | archive)
  pok (json)
  pok (delete) <ID>
  pok (push)   <URL>  <TAGS>
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from auth import authenticate
from docopt import docopt
from pprint import pprint
from const import *
from p import __version__
import requests
import json


def pull_all(command="ls", count=DEFAULT_COUNT, state="all", link_flag=False):
    """
    Return both unread and archived items
    A shameless ripoff of https://getpocket.com/developer/docs/v3/retrieve :P
    """
    PAYLOAD["count"] = count
    PAYLOAD["state"] = state
    PAYLOAD["sort"] = "newest"
    if command == "fav":
        state = "favorites"
        PAYLOAD["favorite"] = True

    print C3 % ("\n_%s_") % (state.upper())

    try:
        res = requests.post(
        GET_URL, data=json.dumps(PAYLOAD), headers=HEADERS, verify=False)
    except:
        raise ("Seems there is something wrong with the config file!")
    return render(res.json()['list'], link_flag=link_flag)


def search(search_term, link_flag=False):
    """
    Return items whose title or url contain the search string.
    """
    print C3 % ("\n_SEARCH RESULTS_")
    PAYLOAD["search"] = search_term
    res = requests.post(
        GET_URL, data=json.dumps(PAYLOAD), headers=HEADERS, verify=False)
    return render(res.json()['list'], link_flag=link_flag)


def json_view():
    """
    Used for debugging and analyzing.
    """
    print C3 % ("\n_JSON VIEW_")
    PAYLOAD["count"] = 5
    return requests.post(GET_URL, data=json.dumps(PAYLOAD), headers=HEADERS, verify=False).json()


def delete_item(item_id):
    """
    Deletes items with a given item id.
    """
    PAYLOAD["actions"] = [{"action": "delete", "item_id": str(item_id)}]
    res = requests.post(
        DELETE_URL, data=json.dumps(PAYLOAD), headers=HEADERS, verify=False).json()
    print C3 % ("<Item : %s> has been deleted!") % (item_id)


def push_item(URL, TAGS):
    """
    Pushes items with a given item id and comma separated tags.
    """
    PAYLOAD["url"] = URL
    PAYLOAD["tags"] = TAGS
    res = requests.post(
        ADD_URL, data=json.dumps(PAYLOAD), headers=HEADERS, verify=False).json()
    print C3 % ("Your ITEM has been added.")


def tag_item(tag_name, link_flag=False):
    """
    Returns Items tagged with tag_name
    ie. tag-name: django will return items tagged django.
    """
    print C3 % ("\n_TAGGED RESULTS_")
    PAYLOAD["tag"] = tag_name
    res = requests.post(
        GET_URL, data=json.dumps(PAYLOAD), headers=HEADERS, verify=False)
    if res.json()['status'] == 2:
        print C3 % ("Invalid tag: Tag not found!")
        exit()
    return render(res.json()['list'], link_flag=link_flag)


def arrange(json_list):
    """
    Returns a json list in order of time stamp.
    """
    j_list = []
    max_title_len = 0
    for key in json_list.keys():
        tupl = (json_list[key]['time_added'], json_list[key])
        j_list.append(tupl)
        max_title_len = max(
            max_title_len, len(json_list[key]['resolved_title']))
    sorted_list = sorted(j_list, key=lambda x: x[0], reverse=True)
    json_list = [x[1] for x in sorted_list]
    return json_list


def render(json_dict, link_flag=False):
    """
    All of the rendering to the prompt is done here.
    """
    json_list = arrange(json_dict)  # arrange with respect to timestamps
    for i in json_list:
        a = C1 % (i['resolved_title'].replace("  ", ""))
        b = C4 % (i['resolved_url'])
        id = i['item_id']
        if link_flag:
            print a  # + " : " + b
            # OR
            b = C2 % (i['resolved_url'])
            print b

        else:
            print a + " " + id


def main():
    """
    Pok is a terminal cli to handle your pocket. Mostly has things
    the chrome extension does not provide.
    """
    arguments = docopt(__doc__, version=__version__)
    count = DEFAULT_COUNT
    conf = authenticate()
    PAYLOAD['access_token'] = conf['token']  # see auth.py to know the process
    # print arguments
    # print PAYLOAD
    if arguments['ls']:
        if arguments['COUNT']:
            count = arguments['COUNT']
        pull_all(command='ls', count=count)
    elif arguments['list']:
        if arguments['COUNT']:
            count = arguments['COUNT']
        pull_all(command='list', count=count, link_flag=True)
    # listing archive and unread
    elif arguments['arcv']:
        pull_all(state="archive", link_flag=False)
    elif arguments['archive']:
        pull_all(state="archive", link_flag=True)
    elif arguments['unr']:
        pull_all(state="unread", link_flag=False)
    elif arguments['unread']:
        pull_all(state="unread", link_flag=True)
    # listing favourite item
    elif arguments['fav']:
        pull_all(command="fav", link_flag=False)
    elif arguments['favourite']:
        pull_all(command="fav", link_flag=True)
    # search via tags and name
    elif arguments['search'] and arguments['<NAME>']:
        search(arguments['<NAME>'], link_flag=True)
    elif arguments['sh'] and arguments['<NAME>']:
        search(arguments['<NAME>'], link_flag=False)
    elif arguments['tag'] and arguments['<NAME>']:
        tag_item(arguments['<NAME>'], link_flag=True)
    elif arguments['t'] and arguments['<NAME>']:
        tag_item(arguments['<NAME>'], link_flag=False)
    # Delete and add an item
    elif arguments['delete'] and arguments['<ID>']:
        delete_item(arguments['<ID>'])
    elif arguments['push'] and arguments['<URL>']:
        push_item(arguments['<URL>'], arguments['<TAGS>'])
    # For testing purpose
    elif arguments['json']:
        pprint(json_view())
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
