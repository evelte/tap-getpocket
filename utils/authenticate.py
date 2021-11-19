import requests
import os
import pathlib
import json
import logging


CONSUMER_KEY = '99548-b00cce06b8a12a1908537110'
REDIRECT_URI = "http://www.google.com"

HEADERS = {'Content-Type': 'application/json',
           "X-Accept": "application/json"}

def get_request_token():

    url = 'https://getpocket.com/v3/oauth/request'
    json = {'consumer_key': CONSUMER_KEY,
            'redirect_uri': REDIRECT_URI}

    r = requests.post(url=url, json=json, headers=HEADERS)
    data = r.json()
    code = data['code']
    print(r.status_code)
    return code


def authorize_app(code):

    authorization_url = 'https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}'.format(code,
                                                                                                       REDIRECT_URI)

    while True:
        print(authorization_url)
        input('press enter after authorizing')

        url = 'https://getpocket.com/v3/oauth/authorize'
        json = {'consumer_key': '99548-b00cce06b8a12a1908537110',
                'code': code}

        r = requests.post(url=url, json=json, headers=HEADERS)
        print(r.status_code)
        status_code = r.status_code

        if status_code == 200:
            break
        elif status_code == 429:
            print(r.headers)
            # https://getpocket.com/developer/docs/rate-limits
            print('Too many requests, exiting flow. Please try again later')
            exit()
        else:
            print('Authorization was not successful, please try again')
    data = r.json()
    access_token = data['access_token']
    return access_token


def test_authentication(access_token):
    # api-endpoint
    URL = "https://getpocket.com/v3/get"
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'Content-Type': 'application/json',
              'consumer_key': CONSUMER_KEY,
              'access_token': access_token,
              'count': 1}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)
    if r.status_code == 200:
        return True
    else:
        return False


def run_authentication_flow():
    code = get_request_token()
    access_token = authorize_app(code)
    return access_token


def search_config_file(file_name='../.env'):
    if os.path.exists(file_name) and pathlib.Path(file_name):
        print('found config file')
        with open(file_name, "r") as f:
            keys = []
            for line in f.readlines():
                try:
                    key, value = line.split('=')
                    keys.append(key)
                except ValueError:
                    # syntax error
                    pass
        if 'TAP_GETPOCKET_ACCESS_TOKEN' in keys:
            print('access token already available, doing nothing')
            token_found = True
        else:
            token_found = False
        return file_name, token_found
    else:
        return None, None


if __name__ == '__main__':
    config_file, token_found = search_config_file()
    if config_file and token_found:
        print('nothing to do here')
    else:
        access_token = run_authentication_flow()
        if not access_token:
            raise RuntimeError('Authentication flow was not successful')
        if config_file:
            with open("../.env", "a", encoding='utf-8') as f:
                f.write("TAP_GETPOCKET_ACCESS_TOKEN={}".format(access_token))
        else:
            with open("../.env", "w", encoding='utf-8') as f:
                f.write("TAP_GETPOCKET_ACCESS_TOKEN={}".format(access_token))
        print('config file updated ({})'.format(access_token))
