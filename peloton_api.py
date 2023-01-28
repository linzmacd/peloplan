import requests
# from flask import session
import crud

session = {}
session['cookie'] = {'peloton_session_id': 'de69fb0867cd439d9470784aa3328505'}

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


def get_categories():
    '''Gets list of categories.'''
    endpoint = 'api/v2/ride/archived'
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, cookies=session['cookie'])
    categories = response.json()['class_types']

    return categories


def get_workout_details(workout_id):
    '''Gets details of workout with specified id.'''
    endpoint = 'api/ride/' + workout_id + '/details'
    api_url = BASE_URL + endpoint
    response = requests.get(api_url, cookies=session['cookie'])
    workout_details = response.json()

    return workout_details


def query_database():
    '''Returns list of workouts with specified filters'''
    endpoint = 'api/v2/ride/archived'
    
    # test data
    discipline = 'cycling'
    limit = 18
    page = 0
    duration = 900
    # instructor_id = crud.get_instructor_id('Ben Alldis')
    instructor_id = 'c0a9505d8135412d824cf3c97406179b'
    # class_type_id = crud.get_category_id('Music', discipline)
    category_id = 'c87e20095d80463db5ce04df7fe2b989'
    favorite = True
    completed = True
    sort = 'top_rated' # original_air_time*, popularity, difficulty, trending
    descending = True # True* False when easiest

    params = {
        'browse_category': discipline,
        'content_format': ['audio', 'video'],
        'limit': 18,
        'duration': duration,
        'instructor_id': instructor_id,
        'class_type_id': category_id,
        # 'super_genre_id': '',
        'is_favorite_ride': favorite,
        'has_workout': completed,
        'sort_by': sort,
        'desc': descending,
        }
    
    # query_string = (
    #     f'?browse_category={discipline}&content_format=audio,video'
    #     f'&limit={limit}&page={page}&duration={duration}'
    #     f'&instructor_id={instructor_id}'
    #     f'&class_type_id={category_id}'
    #     # f'&super_genre_id=c06217bbe61f485094cfe62d098b3bf8'
    #     f'&is_favorite_ride={favorite}&has_workout={completed}'
    #     f'&sort_by={sort}&desc={descending}'
    #     )
    
    api_url = BASE_URL + endpoint #+ query_string
    response = requests.get(api_url, params=params, cookies=session['cookie'])
    workout_results = response.json()['data']

    return workout_results



    # https://api.onepeloton.com/api/v2/ride/archived?browse_category=cycling&content_format=audio,video&limit=18&page=0&duration=600,1800&instructor_id=c0a9505d8135412d824cf3c97406179b,7f3de5e78bb44d8591a0f77f760478c3&class_type_id=c87e20095d80463db5ce04df7fe2b989,59a49f882ea9475faa3110d50a8fb3f3&super_genre_id=c06217bbe61f485094cfe62d098b3bf8,7afdd1462d474005841e9a6a403229f1&is_favorite_ride=true&has_workout=false&sort_by=top_rated&desc=true
    

    