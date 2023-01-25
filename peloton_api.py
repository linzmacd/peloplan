import requests
from flask import session


BASE_URL = 'https://api.onepeloton.com/'

def check_session_id(session_id):
    '''Checks whether session_id is authorized.'''
    endpoint = 'auth/check_session'
    cookie = {'peloton_session_id': session_id}
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, cookies=cookie)    
    auth_details = response.json()

    return auth_details['is_authed']


def get_session_id(login_credentials):
    '''Gets session cookie for Peloton API.'''
    endpoint = 'auth/login'
    api_url = BASE_URL + endpoint
    response = requests.post(api_url, json=login_credentials)
    auth_details = response.json()
    
    return auth_details


def get_instructors():
    '''Gets list of instructors.'''
    print('peloton_api.get_instructors is running.')
    endpoint = "api/instructor"
    query_string = "?limit=100"
    api_url = BASE_URL + endpoint + query_string
    response = requests.get(api_url, cookies=session['cookie'])
    instructors = response.json()['data']

    return instructors


def get_categories():
    '''Gets list of categories.'''
    endpoint = 'api/v2/ride/archived'
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, cookies=session['cookie'])
    categories = response.json()['class_types']

    return categories
    