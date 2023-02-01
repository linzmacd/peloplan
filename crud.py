from model import (db, User, Sched_Workout, Workout, 
                   Instructor, Category, connect_to_db)
import peloton_api
from datetime import datetime


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
    return User.query.filter(User.email == email).first()


def get_user_by_id(user_id):
    '''Returns user object at specified user_id.'''
    return User.query.get(user_id)


def add_auth_details(user_id, auth_details):
    '''Adds session_id to specified user_id.'''
    user = get_user_by_id(user_id)
    user.peloton_user_id = auth_details['user_id']
    user.session_id = auth_details['session_id']
    db.session.commit()


########## INSTRUCTORS ######################

def verify_instructors():
    '''Verifies instructors table up-to-date.'''
    instructors = peloton_api.get_instructors()
    for instructor in instructors:
        instructor_id = instructor['id']
        in_db = bool(Instructor.query.get(instructor_id))
        if not in_db:
            instructor_name = instructor['name']
            new_instructor = Instructor(instructor_id = instructor_id,
                                        instructor_name = instructor_name)
            db.session.add(new_instructor)
    db.session.commit()


def get_instructors():
    '''Returns dictionary of all instructors by id.'''
    instructor_objs =  Instructor.query.order_by(Instructor.instructor_name).all()
    instructor_dict = {}
    for instructor in instructor_objs:
        instructor_dict[instructor.instructor_name] = instructor.instructor_id

    return instructor_dict


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
                     discipline, workout_id=None, completed=False):
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
                                  completed = completed)
    db.session.add(sched_workout)
    db.session.commit()


def update_workout(user_id, sched_date, sched_order, workout_id):
    '''Adds specific workout to workout object.'''
    workout = get_workout(user_id, sched_date, sched_order)
    if not bool(Workout.query.get(workout_id)):
            workout_details = peloton_api.get_workout_details(workout_id)
            add_workout(workout_details)
    workout.workout_id = workout_id
    db.session.commit()


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
            'date': workout.sched_date.strftime("%Y-%m-%d"),
            'order': workout.sched_order,
            'discipline': workout.discipline, 
            'completed': workout.completed,
        }
        if workout.workout.category == 'Freestyle':
            url = f'https://members.onepeloton.com/profile/workouts/{workout.workout_id}'
        else:
            url = (f'https://members.onepeloton.com/classes/cycling?'
                   f'modal=classDetailsModal&classId={workout.workout_id}')
        if workout.workout_id:
            workout_dict['title'] = workout.workout.title
            workout_dict['instructor'] = workout.workout.instructor
            workout_dict['url'] = url
        else:
            if workout.discipline == 'caesar':
                workout_dict['title'] = 'Rowing'
            elif workout.discipline == 'caesar_bootcamp':
                workout_dict['title'] = "Rowing Bootcamp"
            else:
                workout_dict['title'] = workout.discipline.title()
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


# def sync_with_peloton(user_id):
#     '''Adds new completed workouts from Peloton.'''
#     workout_history = peloton_api.get_workout_history(user_id)
#     index_counter = 0
#     for workout in reversed(workout_history):
#         workout_date = datetime.fromtimestamp(workout['created']).strftime('%Y-%m-%d')
#         discipline = workout['fitness_discipline']
#         try: 
#             workout_id = workout['peloton']['ride']['id']
#         except TypeError:
#             workout_id = None
#         # check to see if match for specific workout on schedule
#         sched_workout = check_workout_id(user_id, workout_date, workout_id)
#         if sched_workout:
#             sched_workout.completed = True
#             print(f'{index_counter} - Workout {sched_workout.sched_order} on {sched_workout.sched_date} marked as completed')
#             index_counter += 1
#         else:
#             # check to see if workout is in db and add, if necessary
#             if not bool(Workout.query.get(workout_id)):
#                 try:
#                     workout_details = peloton_api.get_workout_details(workout_id)
#                     add_workout(workout_details)
#                     print(f"{index_counter} - {workout_details['ride']['title']} added to db")
#                 except TypeError:
#                     sched_order = get_order(user_id, workout_date)
#                     schedule_workout(user_id, workout_date, sched_order, discipline)
#                     print(f"{index_counter} - (Type Error) Just Workout added to db")     
#             # check to see if match for generic workout on schedule 
#             sched_discipline = check_workout_discipline(user_id, workout_date, discipline)
#             if sched_discipline:
#                 sched_discipline.workout_id = workout_id
#                 sched_discipline.completed = True
#                 print(f'{index_counter} - Workout {sched_discipline.sched_order} on {sched_discipline.sched_date} updated and marked as completed')
#                 index_counter += 1    
#             # otherwise make new completed workout on schedule
#             else:
#                 sched_order = get_order(user_id, workout_date)
#                 schedule_workout(user_id, workout_date, sched_order, 
#                                  discipline, workout_id, True)
#                 print(f'{index_counter} - New Workout added on {workout_date}')
#                 index_counter += 1    

#     db.session.commit()

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
            # if class is already on schedule
            sched_workout = check_workout_id(user_id, workout_date, workout_id)
            if sched_workout:
                sched_workout.completed = True
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
                    sched_discipline.completed = True
                    print(f'{index_counter} - Workout {sched_discipline.sched_order} on {sched_discipline.sched_date} updated and marked as completed')
                    index_counter += 1    
                # otherwise make new completed workout on schedule
                else:
                    sched_order = get_order(user_id, workout_date)
                    schedule_workout(user_id, workout_date, sched_order, 
                                     discipline, workout_id, True)
                    print(f'{index_counter} - New Workout added on {workout_date}')
                    index_counter += 1    
        elif workout_type == 'freestyle':
            workout_title = workout_title = workout['title']
            workout_id = workout['id']
            # if not in db
            if not Workout.query.get(workout_id):
                duration = workout['ride']['duration']
                workout_id = add_freestyle_workout(workout_id, discipline,
                                                   workout_title, duration)
                # check whether workout matches generic workout
                sched_discipline = check_workout_discipline(user_id, workout_date, discipline)
                if sched_discipline:
                    sched_discipline.workout_id = workout_id
                    sched_discipline.completed = True
                    print(f'{index_counter} - Freestyle Workout {sched_discipline.sched_order} on {sched_discipline.sched_date} updated and marked as completed')
                    index_counter += 1
                else:
                    sched_order = get_order(user_id, workout_date)
                    schedule_workout(user_id, workout_date, sched_order, 
                                    discipline, workout_id, True)
                    print(f'{index_counter} - New Freestyle Workout added on {workout_date}')
                    index_counter += 1   
        else:
            print("NEW WORKOUT TYPE!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    db.session.commit()


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
    '''Creates a new workout object and returns workout_id.'''
    workout = Workout(workout_id = workout_id,
                      discipline = discipline, 
                      category = 'Freestyle', 
                      instructor = None, 
                      title = workout_title, 
                      duration = duration)
    db.session.add(workout)
    db.session.commit()

    return workout_id


if __name__ == '__main__':
    from server import app
    connect_to_db(app)