'''Server for movie ratings app.'''

from flask import (Flask, render_template, request, 
                   flash, session, redirect, jsonify)
from model import connect_to_db, db
import crud, peloton_api
from jinja2 import StrictUndefined
from datetime import date


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined



# Routes and view functions
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

    # check to see if email in use
    user = crud.get_user_by_email(email)
    if user:
        flash('Email already in use.')
    # if not, creates new user
    else: 
        crud.create_user(fname, lname, email, password)
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
        if user.password == password:
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
    # if authorized, add to flask session
    if auth_status:
        session['cookie'] = {'peloton_session_id': session_id}
        return redirect('/update-databases')
    else:
        return redirect('/peloton-login')
    

@app.route('/peloton-login')
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
    '''Syncs with Peloton to verify instructors, and categories.'''
    crud.verify_instructors()
    crud.verify_categories()

    return redirect('/peloton-sync')


@app.route('/peloton-sync')
def sync_with_peloton():
    '''Syncs with Peloton to verify workout history.'''
    crud.sync_with_peloton(session['user_id'])

    return redirect('/peloplan')


@app.route('/peloplan/schedule')
def get_schedule():
    '''Gets schedule data for populating calendar'''
    schedule = crud.get_schedule(session['user_id'])
 
    return jsonify(schedule)


@app.route('/peloplan')
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


# @app.route('/peloplan/init-date')
# def get_pp_start_date():
#     '''Returns the initial date for the calendar.'''
#     initial_date = session.get('pp_start_date', date.today().strftime('%Y-%m-%d'))

#     return jsonify(initial_date)


@app.route('/peloplan-weekly')
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


@app.route('/workout-selection/<workout_date>/<sched_order>/<discipline>', methods=['POST'])
def select_filtered_workout(workout_date, sched_order, discipline):
    '''Filters workout results.'''
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
def show_saved_schedules():
    '''Displays all user's saved schedules'''
    user = crud.get_user_by_id(session['user_id'])
    schedules = crud.get_user_schedules(session['user_id'])

    return render_template('schedules.html',
                           fname = user.fname,
                           schedules = schedules)


@app.route('/public-schedules')
def show_public_schedules():
    '''Displays all public saved schedules'''
    schedules = crud.get_public_schedules()

    return render_template('schedules-public.html',
                           schedules = schedules)


@app.route('/save-schedule', methods=['POST'])
def save_schedule():
    '''Saves a schedule to database.'''
    visibility = request.json.get('visibility')
    sched_name = request.json.get('schedName')
    start_date = request.json.get('startDate')
    end_date = request.json.get('endDate')
    save_type = request.json.get('saveType')
    notes = request.json.get('notes')

    return jsonify(crud.save_schedule(session['user_id'], visibility, sched_name, 
                                      start_date, end_date, save_type, notes))


@app.route('/get-saved-schedules')
def get_saved_schedules():
    '''Retrieves user's saved schedules.'''
    return jsonify(crud.get_user_schedules(session['user_id']))


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
            print(details)
            # details = peloton_api.get_workout_details(workout['workout_id'])
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
    print(storage_id)
    
    return jsonify(crud.delete_saved_schedule(storage_id))


@app.route('/log-out')
def log_out():
    for key in list(session.keys()):
        session.pop(key)

    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)