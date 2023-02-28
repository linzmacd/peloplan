'''Server for PeloPlan app.'''

from flask import (Flask, render_template, request, 
                   flash, session, redirect, jsonify)
from model import connect_to_db
from jinja2 import StrictUndefined
from passlib.hash import argon2
import crud, peloton_api
from datetime import date
from functools import wraps


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined



# Routes and view functions
def logged_in(f):
    '''Checks that user is logged in.'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id', False):
            flash('Please log in to view PeloPlan.')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def homepage():
    '''Renders PeloPlan homepage.'''
    return render_template('homepage.html')


@app.route('/create-account', methods=['POST'])
def create_account():
    '''Creates new PeloPlan user account.'''
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    repeat_pw = request.form.get('confirm')
    hashed = argon2.hash(password)

    # check to see if email in use
    user = crud.get_user_by_email(email)
    if user:
        flash('Email already in use.')
    # check to make sure passwords match
    elif password != repeat_pw:
        flash('Passwords do not match.')
    # creates new user with hashed password
    else: 
        crud.create_user(fname, lname, email, hashed)
        flash('Account created! Please log in to continue.')

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    '''Logs in to PeloPlan user account.'''
    email = request.form.get('email')
    password = request.form.get('password')

    # check to see if email in use
    user = crud.get_user_by_email(email)
    if user:
        # check to see if password correct
        if argon2.verify(password, user.password):
            flash('Logged in to PeloPlan!')
            session['user_id'] = user.user_id
            # check for session id in db
            session_id = user.session_id
            if not session_id:
                return redirect('/peloton-login')
            return redirect(f'/check-cookies/{session_id}')
        else:
            flash('Incorrect password.')
    else:
        flash('Incorrect email.')

    return redirect('/')

@app.route('/check-cookies/<session_id>')
def check_session_cookie(session_id):
    '''Checks auth status of session id.'''
    auth_status = peloton_api.check_session_id(session_id)
    # if authorized, add Peloton cookie to flask session
    if auth_status:
        session['cookie'] = {'peloton_session_id': session_id}
        return redirect('/update-databases')
    else:
        return redirect('/peloton-login')
    

@app.route('/peloton-login')
@logged_in
def peloton_login():
    '''Renders Peloton Login page.'''
    return render_template('peloton-login.html')


@app.route('/peloton-login', methods=['POST'])
def get_peloton_cookie():
    '''Logs in to Peloton to get session_id.'''
    peloton_username = request.form.get('peloton_username')
    peloton_password = request.form.get('peloton_password')
    login_credentials = {'username_or_email': peloton_username, 
                         'password': peloton_password}
    try:
        auth_details = peloton_api.get_session_id(login_credentials)
        session['cookie'] = {'peloton_session_id': auth_details['session_id']}
    except:
        flash('Incorrect Peloton credentials.')
        return redirect('/peloton-login')
    # add auth_details to user in db
    user_id = session['user_id']
    crud.add_auth_details(user_id, auth_details)

    return redirect('/update-databases')


@app.route('/update-databases')
def custodial_work():
    '''Syncs with Peloton to verify instructors and categories.'''
    crud.verify_instructors()
    crud.verify_categories()

    return redirect('/peloton-sync')


@app.route('/peloton-sync')
def sync_with_peloton():
    '''Syncs with Peloton to verify workout history.'''
    crud.sync_with_peloton_csv(session['user_id'])

    return redirect('/peloplan')


@app.route('/full-peloton-sync')
def full_sync_with_peloton():
    '''Syncs with Peloton to get entire workout history.'''
    crud.full_sync_with_peloton_csv(session['user_id'])

    return jsonify(True)


@app.route('/peloplan/schedule')
def get_schedule():
    '''Gets schedule data for populating calendar'''
    schedule = crud.get_schedule(session['user_id'])
 
    return jsonify(schedule)


@app.route('/peloplan')
@logged_in
def display_peloplan():
    '''Shows monthly calendar.'''
    initial_date = session.get('pp_start_date', date.today().strftime('%Y-%m-%d'))
    user = crud.get_user_by_id(session['user_id'])
    schedules = crud.get_user_schedules(session['user_id'])

    return render_template('peloplan.html',
                           initial_date = initial_date,
                           user_fname = user.fname,
                           schedules = schedules)


@app.route('/redirect/peloplan')
def re_redirect():
    '''Redirects to PeloPlan for purpose of reloading on correct date.'''
    return redirect('/peloplan')


@app.route('/peloplan-weekly')
@logged_in
def display_weekly_peloplan():
    '''Shows weekly calendar.'''
    initial_date = session.get('pp_start_date', date.today().strftime('%Y-%m-%d'))
    user = crud.get_user_by_id(session['user_id'])
    schedules = crud.get_user_schedules(session['user_id'])
    
    return render_template('peloplan-weekly.html',
                           initial_date = initial_date,
                           user_fname = user.fname,
                           schedules = schedules)


@app.route('/redirect/peloplan-weekly')
def re_redirect_weekly():
    '''Redirects to PeloPlan for purpose of reloading on correct date.'''
    return redirect('/peloplan-weekly')


@app.route('/peloplan-list')
@logged_in
def display_peloplan_as_list():
    '''Shows a weekly list.'''
    initial_date = session.get('pp_start_date', date.today().strftime('%Y-%m-%d'))
    user = crud.get_user_by_id(session['user_id'])
    schedules = crud.get_user_schedules(session['user_id'])
    
    return render_template('peloplan-list.html',
                           initial_date = initial_date,
                           user_fname = user.fname,
                           schedules = schedules)


@app.route('/redirect/peloplan-list')
def re_redirect_list():
    '''Redirects to PeloPlan for purpose of reloading on correct date.'''
    return redirect('/peloplan-list')


@app.route('/add-generic/<workout_date>/<sched_order>/<discipline>')
def add_generic_workout(workout_date, sched_order, discipline):
    '''Adds generic workout to PeloPlan'''
    session['pp_start_date'] = workout_date
    
    return jsonify(crud.schedule_workout(session['user_id'], workout_date, 
                                         sched_order, discipline))


@app.route('/workout-selection/<workout_date>/<sched_order>/<discipline>')
@logged_in
def select_workout(workout_date, sched_order, discipline):
    '''Allows user to select specific workout.'''
    instructors = crud.get_instructors_by_discipline(discipline)
    categories = crud.get_discipline_categories(discipline)
    results = peloton_api.query_database(discipline = discipline)

    return render_template('/workouts.html',
                           workout_date = workout_date,
                           sched_order = sched_order,
                           discipline = discipline,
                           instructors = instructors,
                           categories = categories,
                           results = results)


@app.route('/workout-selection/filter', methods=['POST'])
def filter_workout():
    '''Filters workout results.'''
    discipline = request.json.get('discipline')
    duration = request.json.get('duration', None)
    instructor = request.json.get('instructor', None)
    category = request.json.get('category', None)
    bookmarked = request.json.get('bookmarked', None)
    completed = request.json.get('completed', None)
    sortby = request.json.get('sortby', 'original_air_time')

    results = peloton_api.query_database(discipline = discipline,
                                         duration = duration,
                                         instructor = instructor,
                                         category = category, 
                                         bookmarked = bookmarked, 
                                         completed = completed, 
                                         sortby = sortby)

    return jsonify(results)


@app.route('/workout-selection/change-page', methods=['POST'])
def change_page():
    '''Retrieves next page of workout results.'''
    discipline = request.json.get('discipline')
    duration = request.json.get('duration', None)
    instructor = request.json.get('instructor', None)
    category = request.json.get('category', None)
    bookmarked = request.json.get('bookmarked', None)
    completed = request.json.get('completed', None)
    sortby = request.json.get('sortby', 'original_air_time')
    page = request.json.get('page')

    results = peloton_api.query_database(discipline = discipline,
                                         duration = duration,
                                         instructor = instructor,
                                         category = category, 
                                         bookmarked = bookmarked, 
                                         completed = completed, 
                                         sortby = sortby,
                                         page = page)

    return jsonify(results)


@app.route('/add-class/<workout_date>/<sched_order>/<discipline>/<workout_id>')
def add_workout(workout_date, sched_order, discipline, workout_id):
    '''Adds specific workout to PeloPlan.'''
    workout = crud.get_workout(session['user_id'], workout_date, sched_order)
    if workout: 
        crud.update_workout(session['user_id'], workout_date, 
                            sched_order, workout_id)
    else:
        crud.schedule_workout(session['user_id'], workout_date, 
                              sched_order, discipline, workout_id)
    session['pp_start_date'] = workout_date

    return redirect('/peloplan')


@app.route('/get-order/<workout_date>')
def get_order(workout_date):
    '''Returns order number for next workout'''
    return jsonify(crud.get_order(session['user_id'], workout_date))


@app.route('/move-up/<workout_date>/<sched_id>')
def move_up(workout_date, sched_id):
    '''Moves a specified class up in order.'''
    session['pp_start_date'] = workout_date
    return jsonify(crud.move_up_in_order(sched_id))


@app.route('/move-down/<workout_date>/<sched_id>')
def move_down(workout_date, sched_id):
    '''Moves a specified workout down in order.'''
    session['pp_start_date'] = workout_date
    return jsonify(crud.move_down_in_order(sched_id))


@app.route('/delete/<workout_date>/<sched_id>')
def delete(workout_date, sched_id):
    '''Deletes a workout from the schedule.'''
    session['pp_start_date'] = workout_date
    return jsonify(crud.delete_workout(sched_id))


@app.route('/saved-schedules')
@logged_in
def show_saved_schedules():
    '''Displays all user's saved schedules'''
    user = crud.get_user_by_id(session['user_id'])
    schedules = crud.get_user_schedules(session['user_id'])

    return render_template('schedules.html',
                           fname = user.fname,
                           schedules = schedules)


@app.route('/public-schedules')
@logged_in
def show_public_schedules():
    '''Displays all public saved schedules'''

    return render_template('schedules-public.html')


@app.route('/save-schedule', methods=['POST'])
def save_schedule():
    '''Saves a schedule to database.'''
    visibility = request.json.get('visibility')
    sched_name = request.json.get('schedName')
    start_date = request.json.get('startDate')
    end_date = request.json.get('endDate')
    save_type = request.json.get('saveType')
    description = request.json.get('description')

    return jsonify(crud.save_schedule(session['user_id'], visibility, sched_name, 
                                      start_date, end_date, save_type, description))


@app.route('/get-public-schedules')
def get_public_schedules():
    '''Retrieves public schedules.'''
    return jsonify(crud.get_public_schedule_list(session['user_id']))


@app.route('/load-schedule', methods=['POST'])
def load_schedule():
    '''Loads a schedule from database.'''
    storage_id = request.json.get('storageId')
    start_date = request.json.get('startDate')
    session['pp_start_date'] = start_date

    return jsonify(crud.load_schedule(session['user_id'], storage_id, start_date))


@app.route('/delete-range', methods=['POST'])
def delete_range():
    '''Deletes all workouts in specified date range.'''
    start_date = request.json.get('startDate')
    end_date = request.json.get('endDate')
    session['pp_start_date'] = start_date
    
    return jsonify(crud.delete_workouts(session['user_id'], start_date, end_date))


@app.route('/preview-schedule/<storage_id>')
@logged_in
def preview_schedule(storage_id):
    '''Previews a schedule from database.'''
    sample = crud.get_saved_schedule(storage_id)

    return render_template('preview.html',
                           sample = sample)


@app.route('/preview-schedule/<storage_id>/data')
def get_preview_schedule(storage_id):
    '''Gets workouts for a preview schedule.'''
    sample = crud.get_saved_schedule(storage_id)
    workouts = sample.workouts
    for workout in workouts:
        if workout['workout_id']:
            details = crud.get_workout_details(workout['workout_id'])
            workout['title'] = details.title
            workout['url'] = (f'https://members.onepeloton.com/classes/{workout["discipline"]}'
                              f'?modal=classDetailsModal&classId={workout["workout_id"]}')
        else:
            workout['title'] = workout['discipline'].title()
            workout['url'] = None     

    return jsonify(workouts)


@app.route('/delete-schedule', methods=['POST'])
def delete_schedule():
    '''Deletes a saved schedule from database.'''
    storage_id = request.json.get('storageId')
    
    return jsonify(crud.delete_saved_schedule(storage_id))


@app.route('/schedule-like/<storage_id>')
def like_schedule(storage_id):
    '''Likes a schedule.'''    
    return jsonify(crud.like_schedule(session['user_id'], storage_id))


@app.route('/schedule-dislike/<storage_id>')
def dislike_schedule(storage_id):
    '''Dislikes a schedule.'''
    return jsonify(crud.dislike_schedule(session['user_id'], storage_id))


@app.route('/profile')
@logged_in
def show_profile():
    '''Shows user's profile'''
    user = crud.get_user_by_id(session['user_id'])
    followers = crud.get_followers(session['user_id'])
    following = crud.get_following(session['user_id'])

    return render_template('profile.html',
                           user = user,
                           followers = followers,
                           following = following)


@app.route('/find-by-name/<first_name>/<last_name>')
def find_friend_by_name(first_name, last_name):
    '''Returns list of users with the specified name.'''
    return jsonify(crud.get_user_by_name(first_name, last_name))


@app.route('/find-by-email/<email>')
def find_friend_by_email(email):
    '''Returns the user with the specified email.'''
    user = crud.get_user_by_email(email)
    user_dict = {'user_id': user.user_id,
                 'name': f'{user.fname} {user.lname}',
                 'email': user.email}
    
    return jsonify(user_dict)


@app.route('/follow/<friend_id>')
def follow_user(friend_id):
    '''Follows specified user.'''
    return jsonify(crud.follow_user(session['user_id'], friend_id))


@app.route('/unfollow/<friend_id>')
def unfollow_user(friend_id):
    '''Unfollows specified user.'''
    return jsonify(crud.unfollow_user(session['user_id'], friend_id))


@app.route('/workout-stats')
@logged_in
def show_workout_stats():
    '''Shows user's workout stats.'''
    date_today = date.today().strftime('%Y-%m')

    return render_template('metrics.html',
                           date = date_today,
                           measure = 'duration')


@app.route('/workout-stats/<date>/<measure>')
@logged_in
def show_filtered_workout_stats(date, measure):
    '''Shows user's workout stats.'''

    return render_template('metrics.html',
                           date = date,
                           measure = measure)


@app.route('/get-metrics/<date>/<measure>')
def get_metrics(date, measure):
    '''Gets metrics for Workout Stats page.'''
    metrics = crud.get_metrics_by_month(session['user_id'], date[5:], date[0:4])
    data = {}
    data['discipline_data'] = crud.discipline_chart(metrics, measure)
    data['instructor_data'] = crud.instructor_chart(metrics, measure)

    return jsonify(data)


@app.route('/output-stats')
@logged_in
def show_output_stats():
    '''Shows user's output stats over time.'''
    metrics = crud.get_metrics_all_time(session['user_id'])
    output_data = crud.output_chart(metrics)

    return render_template('outputs.html',
                           data = output_data)


@app.route('/get-outputs')
def get_outputs():
    '''Gets metrics for Output page.'''
    metrics = crud.get_metrics_all_time(session['user_id'])
    output_data = crud.output_chart(metrics)

    return jsonify(output_data)


@app.route('/log-out')
def log_out():
    for key in list(session.keys()):
        session.pop(key)

    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    # app.run(host='0.0.0.0', debug=True)
    app.run(host='0.0.0.0')