from model import (db, User, Sched_Workout, Workout, 
                   Instructor, Category,connect_to_db)
import peloton_api


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
        if category['is_active']:
            category_id = category['id']
            in_db = bool(Category.query.get(category_id))
            if not in_db:
                category_name = category['display_name']
                discipline = category['fitness_discipline']
                new_category = Category(category_id = category_id,
                                        category_name = category_name,
                                        discipline = discipline)
                db.session.add(new_category)
    db.session.commit()


def get_discipline_categories(discipline):
    '''Returns dictionary of all categories of a discipline by id.'''
    category_objs =  Category.query.filter(Category.discipline == discipline)\
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


########## WORKOUTS #########################

def add_workout(workout_details):
    '''Creates a new workout object'''
    data = workout_details['ride']
    workout = Workout(workout_id = data['id'],
                      discipline = data['fitness_discipline'], 
                      category = get_category_name(data['ride_type_id']), 
                      instructor = get_instructor_name(data['instructor_id']), 
                      title = data['title'], 
                      duration = data['duration'])
    db.session.add(workout)
    db.session.commit()  



if __name__ == '__main__':
    from server import app
    connect_to_db(app)