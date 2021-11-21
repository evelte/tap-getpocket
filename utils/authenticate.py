"""
This script runs the authentication flow to get the access_token needed to authenticate to the pocket API
In order to execute the script needs the consumer_key provided by the user. They key can be provided via command line
argument. If no argument is provided, the script will prompt the user to insert one on execution

The user can get his consumer key here: https://getpocket.com/developer/apps/
Or create a new one here: https://getpocket.com/developer/apps/new/
"""

import os
import sys
import yaml
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


def find_consumer_key():
    consumer_key = os.environ.get('TAP_GETPOCKET_CONSUMER_KEY', None)
    if consumer_key:
        print('Found consumer key in environment variables')
    else:
        print('No consumer key found in environment variables')
        # check meltano.yml (assuming the script runs from the same path or from utils folder)
        config_file_paths = [os.path.join('..', 'meltano.yml'), 'meltano.yml']
        for config_file in config_file_paths:
            if os.path.exists(config_file):
                with open(config_file) as file:
                    try:
                        extractors_config = yaml.load(file, Loader=yaml.FullLoader)['plugins']['extractors']
                        this_tap = next((item for item in extractors_config if item['name'] == 'tap-getpocket'), None)
                        consumer_key = this_tap.get('config', {}).get('consumer_key', None)
                    except:
                        print('No consumer key found in config file')
                    else:
                        if consumer_key:
                            print('Found consumer key in config file: {}'.format(consumer_key))
                            break
    return consumer_key


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        # consumer key can be provided as argument
        your_consumer_key = args[1]
        print('Using argument as consumer key')
    else:
        # check if consumer key is in environment variables or in meltano.yml
        your_consumer_key = find_consumer_key()
        if not your_consumer_key:
            print('No consumer key found in setup')
            print('Get or create your consumer key here: https://getpocket.com/developer/apps/')
            while not your_consumer_key or your_consumer_key.strip() == '':
                your_consumer_key = input('Please enter your key:')

    your_access_token = run_authentication_flow(your_consumer_key)
    print('\nYou can set your environment variables using:')
    print('export TAP_GETPOCKET_ACCESS_TOKEN={}'.format(your_access_token))
    print('export TAP_GETPOCKET_CONSUMER_KEY={}'.format(your_consumer_key))
    print('\nOr add your credentials to your config.json file:')
    json_content = '''"consumer_key": "{}", "access_token": "{}"'''.format(your_consumer_key, your_access_token)
    print('{'+json_content+'}')
