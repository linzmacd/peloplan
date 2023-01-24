import requests


BASE_URL = 'https://api.onepeloton.com/'

def check_session_id():
    '''Check to see if session_id is authorized.'''
    endpoint = 'auth/check_session'
    query_string = 'peloton_session_id={session_id}'
    api_url = BASE_URL + endpoint + query_string
    response = requests.get(api_url)    
    auth_details = response.json()

    return auth_details['is_authed']


def get_session_id(login_credentials):
    '''Gets session cookie for Peloton API'''
    endpoint = "auth/login"
    api_url = BASE_URL + endpoint
    response = requests.post(api_url, json=login_credentials)
    auth_details = response.json()
    session_id = auth_details["session_id"]
    
    return session_id