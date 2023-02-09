from model import (db, User, Sched_Workout, Comp_Workout, Workout, Schedule, 
                   Instructor, Inst_Disc, Category, connect_to_db)
import peloton_api
from datetime import datetime
from sqlalchemy import func


########## USERS ############################

def create_user(fname, lname, email, password, 
                peloton_user_id=None, session_id=None):
    '''Creates a new user object.'''
    new_user = User(fname = fname, 
                    lname = lname, 
                    email = email, 
                    password = password,
                    peloton_user_id = peloton_user_id,
                    session_id = session_id)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def get_user_by_email(email):
    '''Returns user object if email exists.'''
    return User.query.filter(func.lower(User.email) == func.lower(email)).first()


def get_user_by_name(fname, lname):
    '''Returns list of users with the specified first and last names.'''
    users = User.query.filter(func.lower(User.fname) == func.lower(fname),
                              func.lower(User.lname) == func.lower(lname)).all()
    user_list = []
    for user in users:
        user_list += [{'user_id': user.user_id,
                       'name': f'{user.fname} {user.lname}',
                       'email': user.email}]
        
    return user_list


def get_user_by_id(user_id):
    '''Returns user object at specified user_id.'''
    return User.query.get(user_id)


def add_auth_details(user_id, auth_details):
    '''Adds session_id to specified user_id.'''
    user = get_user_by_id(user_id)
    user.peloton_user_id = auth_details['user_id']
    user.session_id = auth_details['session_id']
    db.session.commit()


def follow_user(user_id, friend_user_id):
    '''Follows another user.'''
    user = User.query.get(user_id)
    friend = User.query.get(friend_user_id)
    user.following.append(friend)
    db.session.commit()
    return True


def unfollow_user(user_id, friend_user_id):
    "Unfollows another user."
    user = User.query.get(user_id)
    friend = User.query.get(friend_user_id)
    user.following.remove(friend)
    db.session.commit()
    return True


def get_followers(user_id):
    '''Returns list of followers.'''
    return User.query.get(user_id).followers


def get_following(user_id):
    '''Returns list of other users that specified user is following.'''
    return User.query.get(user_id).following


########## INSTRUCTORS ######################

def verify_instructors():
    '''Verifies instructors and instructor_disciplines tables up-to-date.'''
    instructors = peloton_api.get_instructors()
    for instructor in instructors:
        instructor_id = instructor['id']
        if not Instructor.query.get(instructor_id):
            instructor_name = instructor['name']
            new_instructor = Instructor(instructor_id = instructor_id,
                                        instructor_name = instructor_name)
            db.session.add(new_instructor)
        instructor_disciplines = instructor['fitness_disciplines']
        for discipline in instructor_disciplines:
            if not Inst_Disc.query.filter(Inst_Disc.instructor_id == instructor_id,
                                          Inst_Disc.discipline == discipline).first():
                new_pairing = Inst_Disc(instructor_id = instructor_id,
                                        discipline = discipline)
                db.session.add(new_pairing)
    db.session.commit()


def get_instructors_by_discipline(discipline=None):
    '''Returns dictionary of all instructors of a discipline by id.'''
    if discipline:
        inst_objs = Inst_Disc.query.options(db.joinedload('instructors'))\
                                   .filter(Inst_Disc.discipline == discipline).all()
    else:
        inst_objs =  Instructor.query.order_by(Instructor.instructor_name).all()
    instructor_dict = {}
    for paring in inst_objs:
        instructor_dict[paring.instructors.instructor_name] = paring.instructor_id

    instructor_names = list(instructor_dict.keys())
    instructor_names.sort()
    sorted_dict = {}
    for name in instructor_names:
        sorted_dict[name] = instructor_dict[name]
    
    return sorted_dict


def get_instructor_name(instructor_id):
    '''Returns instructor name at specified instructor_id.'''
    return Instructor.query.get(instructor_id).instructor_name


def get_instructor_id(name):
    '''Returns instructor_id for specified instructor.'''
    return Instructor.query.filter(Instructor.instructor_name == name)\
                           .first().instructor_id


########## CATEGORIES #######################

def verify_categories():
    '''Verifies categories table up-to-date.'''
    categories = peloton_api.get_categories()
    for category in categories:
        # if category['is_active']:
        category_id = category['id']
        in_db = bool(Category.query.get(category_id))
        if not in_db:
            category_name = category['display_name']
            discipline = category['fitness_discipline']
            is_active = category['is_active']
            new_category = Category(category_id = category_id,
                                    category_name = category_name,
                                    discipline = discipline,
                                    is_active = is_active)
            db.session.add(new_category)
    db.session.commit()


def get_discipline_categories(discipline):
    '''Returns dictionary of all active categories of a discipline by id.'''
    category_objs =  Category.query.filter(Category.discipline == discipline,
                                           Category.is_active == True) \
                                   .order_by(Category.category_name).all()
    category_dict = {}
    for category in category_objs:
        category_dict[category.category_name] = category.category_id

    return category_dict


def get_category_name(category_id):
    '''Returns category name at specified category_id.'''
    return Category.query.get(category_id).category_name


def get_category_id(category_name, discipline):
    '''Returns category_id for specified category.'''
    return Category.query.filter(Category.category_name == category_name,
                                 Category.discipline == discipline)\
                         .first().category_id


########## SCHED_WORKOUTS ###################

def schedule_workout(user_id, sched_date, sched_order, 
                     discipline, workout_id=None, completed_id=None):
    '''Creates a new scheduled workout object.'''
    if not workout_id == None:
        # add workout to db if new
        if not bool(Workout.query.get(workout_id)):
            workout_details = peloton_api.get_workout_details(workout_id)
            add_workout(workout_details)
    sched_workout = Sched_Workout(user_id = user_id, 
                                  sched_date = sched_date,
                                  sched_order = sched_order, 
                                  discipline = discipline,
                                  workout_id = workout_id,
                                  completed_id = completed_id)
    db.session.add(sched_workout)
    db.session.commit()
    return True


def update_workout(user_id, sched_date, sched_order, workout_id):
    '''Adds specific workout to workout object.'''
    workout = get_workout(user_id, sched_date, sched_order)
    if not bool(Workout.query.get(workout_id)):
            workout_details = peloton_api.get_workout_details(workout_id)
            add_workout(workout_details)
    workout.workout_id = workout_id
    db.session.commit()
    return True


def get_schedule(user_id):
    '''Gets schedule for specified user.'''
    schedule =  Sched_Workout.query.options(db.joinedload('workout'))\
                             .filter(Sched_Workout.user_id == user_id)\
                             .order_by(Sched_Workout.sched_date,\
                                       Sched_Workout.sched_order).all()
    schedule_list = []
    for workout in schedule:
        workout_dict = {
            'id': workout.schedule_id,
            'date': workout.sched_date.strftime('%Y-%m-%d'),
            'order': workout.sched_order,
            'discipline': workout.discipline,
            'completed': bool(workout.completed_id)
            }
        # if workout is rowing or a bootcamp, fix discipline name
        if workout.discipline == 'caesar':
            workout_dict['display_discipline'] = 'rowing'
        elif workout.discipline == 'caesar_bootcamp':
            workout_dict['display_discipline'] = 'rowing bootcamp'
        elif workout.discipline == 'bootcamp':
            workout_dict['display_discipline'] = 'tread bootcamp'
        elif workout.discipline == 'bike_bootcamp':
            workout_dict['display_discipline'] = 'bike bootcamp'
        else:
            workout_dict['display_discipline'] = workout.discipline
        # if workout completed, url links to session, otherwise links to class
        if workout.completed_id:
            url = f'https://members.onepeloton.com/profile/workouts/{workout.completed_id}'
        else:
            url = (f'https://members.onepeloton.com/classes/cycling?'
                   f'modal=classDetailsModal&classId={workout.workout_id}')
        # if there is a class assignment, add title and instructor
        if workout.workout_id:
            workout_dict['title'] = workout.workout.title
            workout_dict['instructor'] = workout.workout.instructor
            workout_dict['url'] = url
        else:
            workout_dict['title'] = workout_dict['display_discipline'].title()
            workout_dict['instructor'] = None
            workout_dict['url'] = 0
        schedule_list.append(workout_dict)

    return schedule_list


def get_order(user_id, sched_date):
    '''Returns next slot in order on specified date.'''
    max =  Sched_Workout.query.filter(Sched_Workout.user_id == user_id,
                                      Sched_Workout.sched_date == sched_date)\
                        .order_by(Sched_Workout.sched_order.desc()).first()
    if max:
        next_order = max.sched_order + 1
    else:
        next_order = 1
    return next_order


def get_workout(user_id, sched_date, sched_order):
    '''Returns workout object at specified date and order.'''
    workout =  Sched_Workout.query.filter(Sched_Workout.user_id == user_id,
                                          Sched_Workout.sched_date == sched_date,
                                          Sched_Workout.sched_order == sched_order)
    return workout.first()


def check_workout_id(user_id, workout_date, workout_id):
    '''Returns workout objects matching workout_id on specified date.'''
    workout =  Sched_Workout.query.filter(Sched_Workout.user_id == user_id,
                                          Sched_Workout.sched_date == workout_date,
                                          Sched_Workout.workout_id == workout_id)
    return workout.first()


def check_workout_discipline(user_id, workout_date, discipline):
    '''Returns first workout objects matching discipline on specified date.'''
    workout =  Sched_Workout.query.filter(Sched_Workout.user_id == user_id,
                                          Sched_Workout.sched_date == workout_date,
                                          Sched_Workout.workout_id == None,
                                          Sched_Workout.discipline == discipline)
    return workout.first()


def move_up_in_order(schedule_id):
    '''Moves workout up a position in order for the day.'''
    workout = Sched_Workout.query.get(schedule_id)
    user_id = workout.user_id
    sched_date = workout.sched_date
    sched_order = workout.sched_order
    if sched_order == 1:
        return False
    else:
        prior = Sched_Workout.query.filter(Sched_Workout.user_id == user_id,
                                           Sched_Workout.sched_date == sched_date,
                                           Sched_Workout.sched_order == (sched_order - 1)).first()
        workout.sched_order -= 1
        prior.sched_order += 1
        db.session.commit()
        return True
    
def move_down_in_order(schedule_id):
    '''Moves workout down a position in order for the day.'''
    workout = Sched_Workout.query.get(schedule_id)
    user_id = workout.user_id
    sched_date = workout.sched_date
    sched_order = workout.sched_order
    last_order = get_order(user_id, sched_date) - 1
    if sched_order == last_order:
        return False
    else:
        next = Sched_Workout.query.filter(Sched_Workout.user_id == user_id,
                                          Sched_Workout.sched_date == sched_date,
                                          Sched_Workout.sched_order == (sched_order + 1)).first()
        workout.sched_order += 1
        next.sched_order -= 1
        db.session.commit()
        return True
    

def delete_workout(schedule_id):
    '''Deletes workout from database.'''
    workout = Sched_Workout.query.get(schedule_id)
    user_id = workout.user_id
    sched_date = workout.sched_date
    db.session.delete(workout)
    workouts = Sched_Workout.query.filter(Sched_Workout.user_id == user_id,
                                          Sched_Workout.sched_date == sched_date)\
                                  .order_by(Sched_Workout.sched_order).all()
    for index, workout in enumerate(workouts):
            workout.sched_order = index + 1
    db.session.commit()
    return True


def delete_workouts(user_id, start_date, end_date):
    '''Deletes workouts within a date range from database.'''
    workouts = Sched_Workout.query.filter(Sched_Workout.user_id == user_id,
                                          Sched_Workout.sched_date >= start_date,
                                          Sched_Workout.sched_date <= end_date).all()
    for workout in workouts:
        db.session.delete(workout)
    db.session.commit()
    return True


def sync_with_peloton(user_id):
    '''Adds new completed workouts from Peloton.'''
    workout_history = peloton_api.get_workout_history(user_id)
    index_counter = 0
    for workout in reversed(workout_history):
        workout_date = datetime.fromtimestamp(workout['created']).strftime('%Y-%m-%d')
        discipline = workout['fitness_discipline']
        workout_type = workout['workout_type']
        # if workout is a class or scenic workout
        if workout_type == 'class' or workout_type == 'scenic':
            workout_id = workout['peloton']['ride']['id']
            completed_id = workout['id']
            print(completed_id)
            # if metrics already in db, skip
            if get_metrics(completed_id):
                print('check!')
                continue
            else:
                add_metrics(completed_id,)
                # if class is already on schedule add completed_id
                sched_workout = check_workout_id(user_id, workout_date, workout_id)
                if sched_workout:
                    sched_workout.completed_id = completed_id
                    print(f'{index_counter} - Workout {sched_workout.sched_order} on {sched_workout.sched_date} marked as completed')
                    index_counter += 1
                # if class not on schedule
                else:
                    # check whether workout in db and add if necessary
                    if not Workout.query.get(workout_id):
                        workout_details = peloton_api.get_workout_details(workout_id)
                        add_workout(workout_details)
                        print(f"{index_counter} - {workout_details['ride']['title']} added to db")
                    # check whether workout matches generic workout
                    sched_discipline = check_workout_discipline(user_id, workout_date, discipline)
                    if sched_discipline:
                        sched_discipline.workout_id = workout_id
                        sched_discipline.completed_id = completed_id
                        print(f'{index_counter} - Workout {sched_discipline.sched_order} on {sched_discipline.sched_date} updated and marked as completed')
                        index_counter += 1    
                    # otherwise make new completed workout on schedule
                    else:
                        sched_order = get_order(user_id, workout_date)
                        schedule_workout(user_id, workout_date, sched_order, 
                                        discipline, workout_id, completed_id)
                        print(f'{index_counter} - New Workout added on {workout_date}')
                        index_counter += 1    
        elif workout_type == 'freestyle':
            workout_title = workout['title']
            workout_id = f'{workout_date} / {workout_title}'
            completed_id = workout['id']
            # if metrics already in db, skip
            if get_metrics(completed_id):
                print('check!')
                continue
            else:
                add_metrics(completed_id)
                # if not in db
                if not Workout.query.get(workout_id):
                    duration = workout['ride']['duration']
                    add_freestyle_workout(workout_id, discipline,
                                        workout_title, duration)
                    # check whether workout matches generic workout
                    sched_discipline = check_workout_discipline(user_id, workout_date, discipline)
                    if sched_discipline:
                        sched_discipline.workout_id = workout_id
                        sched_discipline.completed_id = completed_id
                        print(f'{index_counter} - Freestyle Workout {sched_discipline.sched_order} on {sched_discipline.sched_date} updated and marked as completed')
                        index_counter += 1
                    else:
                        sched_order = get_order(user_id, workout_date)
                        schedule_workout(user_id, workout_date, sched_order, 
                                        discipline, workout_id, completed_id)
                        print(f'{index_counter} - New Freestyle Workout added on {workout_date}')
                        index_counter += 1   
        else:
            print('NEW WORKOUT TYPE!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    db.session.commit()


########## COMPLETED WORKOUTS ###############

def add_metrics(completed_id):
    '''Adds metrics to a completed workout.'''
    metrics = peloton_api.get_workout_metrics(completed_id)
    metrics_dict = {'total_output': None,
                    'distance': None,
                    'calories': None,
                    'avg_output': None,
                    'avg_cadence': None,
                    'avg_resistance': None,
                    'avg_speed': None}
    for metric in metrics['summaries']:
        metrics_dict[metric['slug']] = metric['value']
    for metric in metrics['average_summaries']:
        metrics_dict[metric['slug']] = metric['value']
        
    workout  = Comp_Workout(completed_id = completed_id, 
                            duration = metrics['duration'], 
                            total_output = metrics_dict['total_output'], 
                            distance = metrics_dict['distance'], 
                            calories = metrics_dict['calories'],
                            avg_output = metrics_dict['avg_output'], 
                            avg_cadence = metrics_dict['avg_cadence'], 
                            avg_resistance = metrics_dict['avg_resistance'], 
                            avg_speed = metrics_dict['avg_speed'])
    db.session.add(workout)
    db.session.commit()
    return workout


def get_metrics(completed_id):
    '''Returns metrics for completed workout.'''
    return Comp_Workout.query.get(completed_id)


########## WORKOUTS #########################

def add_workout(workout_details):
    '''Creates a new workout object.'''
    data = workout_details['ride']
    try:
        instructor = peloton_api.get_instructor(data['instructor_id'])
    except:
        instructor = None
    workout = Workout(workout_id = data['id'],
                      discipline = data['fitness_discipline'], 
                      category = get_category_name(data['ride_type_id']), 
                      instructor = instructor, 
                      title = data['title'], 
                      duration = data['duration'])
    db.session.add(workout)
    db.session.commit()


def add_freestyle_workout(workout_id, discipline, workout_title, duration):
    '''Creates a new Freestyle workout object.'''
    workout = Workout(workout_id = workout_id,
                      discipline = discipline, 
                      category = 'Freestyle', 
                      instructor = None, 
                      title = workout_title, 
                      duration = duration)
    db.session.add(workout)
    db.session.commit()


def get_workout_details(workout_id):
    '''Returns workout object at specified workout_id'''
    return Workout.query.get(workout_id)


########## SCHEDULES #########################

def create_schedule(creator, visibility, sched_name, start_date, 
                    end_date, sched_type, workouts, description):
    '''Creates a new schedule object.'''
    diff = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
    length = diff.days + 1
    count = len(workouts)
    schedule = Schedule(creator = creator,
                        visibility = visibility, 
                        sched_name = sched_name, 
                        start_date = start_date,
                        end_date = end_date,
                        length = length,
                        sched_type = sched_type,
                        count = count, 
                        workouts = workouts,
                        description = description)
    db.session.add(schedule)
    db.session.commit()
    return schedule


def save_schedule(user_id, visibility, schedule_name, start_date, end_date, save_type, description):
    '''Saves schedule within the specified date range.'''
    schedule = Sched_Workout.query.filter(Sched_Workout.user_id == user_id,
                                          Sched_Workout.sched_date >= start_date,
                                          Sched_Workout.sched_date <= end_date)\
                                  .order_by(Sched_Workout.sched_date,
                                            Sched_Workout.sched_order).all()
    workouts = []
    for workout in schedule:
        workout_id = workout.workout_id
        if (workout_id) and (save_type == 'specific'):
            if '/' in workout_id:
                workout_id = None
            else:
                workout_id = workout.workout_id
        else:
            workout_id = None
        workouts += [{'sched_date': workout.sched_date.strftime('%Y-%m-%d'),
                      'sched_order': workout.sched_order,
                      'discipline': workout.discipline,
                      'workout_id': workout_id}]
    schedule = create_schedule(user_id, visibility, schedule_name, start_date, 
                               end_date, save_type, workouts, description)

    return True


def get_user_schedules(user_id):
    '''Returns schedule objects for specified user.'''
    return Schedule.query.filter(Schedule.creator == user_id).all()


def get_saved_schedule(storage_id):
    '''Returns a specific schedule'''
    return Schedule.query.get(storage_id)


def get_public_schedules():
    '''Returns all public schedules.'''
    return Schedule.query.options(db.joinedload('user'))\
                         .filter(Schedule.visibility == 'public').all()


def load_schedule(user_id, storage_id, load_start_date):
    '''Loads schedule starting at a specified date.'''
    schedule = Schedule.query.get(storage_id)
    save_start_date = datetime.strftime(schedule.start_date,'%Y-%m-%d')
    workouts = schedule.workouts
    if load_start_date == save_start_date:
        for workout in workouts:
            schedule_workout(user_id, workout['sched_date'], workout['sched_order'], 
                             workout['discipline'], workout['workout_id'])
    else:
        load_start_date = datetime.strptime(load_start_date, '%Y-%m-%d').date()
        delta = load_start_date - schedule.start_date
        for workout in workouts:
            save_date = datetime.strptime(workout['sched_date'], '%Y-%m-%d')
            load_date = (save_date + delta).strftime('%Y-%m-%d')
            schedule_workout(user_id, load_date, workout['sched_order'], 
                             workout['discipline'], workout['workout_id'])

    return True


def delete_saved_schedule(storage_id):
    '''Deletes schedule object from database.'''
    schedule = Schedule.query.get(storage_id)
    db.session.delete(schedule)
    db.session.commit()

    return True


if __name__ == '__main__':
    from server import app
    connect_to_db(app)