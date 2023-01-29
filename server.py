'''Server for movie ratings app.'''

from flask import (Flask, render_template, request, 
                   flash, session, redirect, jsonify)
from model import connect_to_db, db
import crud, peloton_api
from jinja2 import StrictUndefined


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
        return redirect('/peloplan')
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

    return redirect('/peloplan')
    

@app.route('/peloplan')
def display_peloplan():
    '''Shows monthly calendar.'''
    # verify instructors and categories
    crud.verify_instructors()
    crud.verify_categories()

    return render_template('peloplan.html')


@app.route('/peloplan/schedule')
def get_schedule():
    '''Gets schedule data for populating calendar'''
    schedule = crud.get_schedule(session['user_id'])
 
    return jsonify(schedule)


@app.route('/<workout_date>/discipline-selection/')
def select_discipline(workout_date):
    '''Allows user to select workout discipline.'''

    return render_template('/disciplines.html',
                           workout_date = workout_date)


@app.route('/<workout_date>/<discipline>')
def add_generic_workout(workout_date, discipline):
    '''Adds generic workout to PeloPlan'''
    order = crud.get_order(session['user_id'],workout_date)
    crud.schedule_workout(session['user_id'], workout_date, order, discipline)
    return redirect('/peloplan')


@app.route('/<workout_date>/<discipline>/workout-selection/')
def select_workout(workout_date, discipline):
    '''Allows user to select specific workout.'''
    instructors = crud.get_instructors()
    categories = crud.get_discipline_categories(discipline)
    results = peloton_api.query_database()

    return render_template('/workouts.html',
                           workout_date = workout_date,
                           discipline = discipline,
                           instructors = instructors,
                           categories = categories,
                           results = results)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)