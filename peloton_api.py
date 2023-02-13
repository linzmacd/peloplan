import requests
from flask import session
from model import connect_to_db
import crud


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
    endpoint = 'api/instructor'
    query_string = '?limit=100'
    api_url = BASE_URL + endpoint + query_string
    response = requests.get(api_url, cookies=session['cookie'])
    instructors = response.json()['data']

    return instructors


def get_instructor(instructor_id):
    '''Get instructor name by id.'''
    endpoint = f'api/instructor/{instructor_id}'
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, cookies=session['cookie'])
    instructor = response.json()

    return instructor['name']


def get_categories():
    '''Gets list of categories.'''
    endpoint = 'api/v2/ride/archived'
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, cookies=session['cookie'])
    categories = response.json()['class_types']

    return categories


def get_workout_history(user_id):
    '''Gets Peloton workout history.'''
    user = crud.get_user_by_id(user_id)
    peloton_user_id = user.peloton_user_id
    endpoint = 'api/user/'+ peloton_user_id + '/workouts'
    params = {
        'joins': 'peloton.ride',
        'limit': 100,
        'page' : 0,
        'sort': '-created'
    }
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, params=params, cookies=session['cookie'])
    workout_list = response.json()['data']

    return workout_list


def get_full_workout_history(user_id):
    '''Gets Peloton workout history.'''
    user = crud.get_user_by_id(user_id)
    peloton_user_id = user.peloton_user_id
    endpoint = 'api/user/'+ peloton_user_id + '/workouts'
    params = {
        'joins': 'peloton.ride',
        'limit': 100,
        'page' : 0,
        'sort': '-created'
    }
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, params=params, cookies=session['cookie'])
    page_count = response.json()['page_count']
    pages = list(range(0,page_count))
    workout_list = []
    for page in pages:
        params = {
            'joins': 'peloton.ride',
            'limit': 100,
            'page' : page,
            'sort': '-created'
        }
        response = requests.get(api_url, params=params, cookies=session['cookie'])
        page_workout_list = response.json()['data']
        workout_list = workout_list + page_workout_list
    print(len(workout_list))

    return workout_list


def get_workout_details(workout_id):
    '''Gets details of workout with specified id.'''
    endpoint = 'api/ride/' + workout_id + '/details'
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, cookies=session['cookie'])
    workout_details = response.json()

    return workout_details


def get_workout_metrics(comp_workout_id):
    '''Gets the metrics from a completed workout.'''
    endpoint = f'api/workout/{comp_workout_id}/performance_graph'
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, cookies=session['cookie'])
    metrics = response.json()

    return metrics


def query_database(discipline, duration=None, instructor=None, 
                   category=None, bookmarked=None, completed=None, 
                   sortby='original_air_time', desc=True, page=0):
    '''Returns list of workouts with specified filters'''
    endpoint = 'api/v2/ride/archived'
    params = {
        'content_format': ['audio', 'video'],
        'limit': 18,
        'page': page
    }

    # corresponding lists of arguments and their corresponding query parameters
    arguments = [discipline, duration, instructor, category, 
                   bookmarked, completed, sortby, desc]
    query_params = ['browse_category', 'duration', 'instructor_id', 
                    'class_type_id', # 'super_genre_id',
                    'is_favorite_ride', 'has_workout', 'sort_by', 'desc']

    # combine query parameter names with args
    for index, argument in enumerate(arguments):
        if argument:
            if argument != '':
                params[query_params[index]] = argument
    
    # if sorting by easiest, correct params
    if params['sort_by'] == 'easiest':
        params['sort_by'] = 'difficulty'
        params['desc'] = False
    
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, params=params, cookies=session['cookie'])
    workout_results = response.json()

    return workout_results



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    

    