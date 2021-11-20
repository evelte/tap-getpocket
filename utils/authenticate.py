"""
This script runs the authentication flow to get the access_token needed to authenticate to the pocket API
In order to execute the script needs the consumer_key provided by the user. They key can be provided via command line
argument. If no argument is provided, the script will prompt the user to insert one on execution

The user can get his consumer key here: https://getpocket.com/developer/apps/
Or create a new one here: https://getpocket.com/developer/apps/new/
"""

import sys
import requests


REDIRECT_URI = "http://www.google.com"

HEADERS = {'Content-Type': 'application/json',
           "X-Accept": "application/json"}


def get_request_token(consumer_key):
    """
    requests access token from API based on provided consumer key
    :param consumer_key: provided by user
    :return: code to use to request access token for API authentication
    """
    url = 'https://getpocket.com/v3/oauth/request'
    json = {'consumer_key': consumer_key,
            'redirect_uri': REDIRECT_URI}

    try:
        r = requests.post(url=url, json=json, headers=HEADERS)
        if r.status_code == 200:
            code = r.json()['code']
        else:
            raise ValueError('Failed to request code. Status code {}'.format(r.status_code))
    except Exception as err:
        print(err)
        raise RuntimeError('Could not get code, authentication flow failed')
    else:
        return code


def authorize_app(consumer_key, code):
    """
    Requests authorization from user via web link. After authorization requests access_token from API
    :param consumer_key: key provided by user
    :param code: code obtained on previous step
    :return: access_token for API authentication
    """
    try:
        auth_url = 'https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}'.format(code, REDIRECT_URI)
        while 'authorization not successful':
            print(auth_url)
            input('Open link above and press enter after authorizing')

            url = 'https://getpocket.com/v3/oauth/authorize'
            json = {'consumer_key': consumer_key,
                    'code': code}

            r = requests.post(url=url, json=json, headers=HEADERS)
            status_code = r.status_code

            if status_code == 200:
                break
            elif status_code == 429:
                # https://getpocket.com/developer/docs/rate-limits
                print('Too many requests, exiting flow. Please try again later')
                exit()
            else:
                print('Authorization was not successful, please try again')
        access_token = r.json()['access_token']
    except Exception as err:
        print(err)
        raise RuntimeError('Could not get access token, authentication flow failed')
    else:
        print('Authentication flow concluded with success')
        print('Your access token is: {}'.format(access_token))
        return access_token


def run_authentication_flow(consumer_key):
    """
    runs complete authentication flow, first getting code and then getting access token using code
    :param consumer_key: provided by user
    :return: access_token for API authentication
    """
    code = get_request_token(consumer_key)
    access_token = authorize_app(consumer_key, code)
    return access_token


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        your_consumer_key = args[1]
    else:
        your_consumer_key = None
        print('Get or create your consumer key here: https://getpocket.com/developer/apps/')
        while not your_consumer_key or your_consumer_key.strip() == '':
            your_consumer_key = input('Please enter your key:')

    your_access_token = run_authentication_flow(your_consumer_key)
    print('you can set your environment variable using:')
    print('export TAP_GETPOCKET_ACCESS_TOKEN={}'.format(your_access_token))
