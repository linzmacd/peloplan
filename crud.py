from model import db, User, Sched_Workout, Workout, connect_to_db


def create_user(fname, lname, email, password):
    '''Creates a new user object.'''
    user = User(fname = fname, 
                lname = lname, 
                email = email, 
                password = password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email):
    '''Returns user object if email exists.'''
    return User.query.filter(User.email == email).first()


def get_user_by_id(user_id):
    '''Returns user object at specified user_id.'''
    return User.query.get(user_id)


def add_session_id(user_id, session_id):
    '''Adds session_id to specified user_id.'''
    user = get_user_by_id(user_id)
    user.session_id = session_id
    db.session.commit()


# def schedule_workout(user_id, sched_date, sched_order, discipline, workout_id):
#     '''Creates a new scheduled workout object.'''
#     sched_workout = Sched_Workout(user_id = user_id, 
#                                   sched_date = sched_date,
#                                   sched_order = sched_order, 
#                                   discipline = discipline,
#                                   workout_id = workout_id)
#     return sched_workout


# def add_workout(workout_id, discipline, category, instructor, title, duration):
#     '''Creates a new workout object'''
#     workout = Workout(workout_id = workout_id,
#                       discipline = discipline, 
#                       category = category, 
#                       instructor = instructor, 
#                       title = title, 
#                       duration = duration)
#     return workout


if __name__ == '__main__':
    from server import app
    connect_to_db(app)