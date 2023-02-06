'''Models for PeloPlan app.'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    '''A user.'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True )
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    peloton_user_id = db.Column(db.String)
    session_id = db.Column(db.String)

    sched_workouts = db.relationship('Sched_Workout', back_populates='user')
    schedules = db.relationship('Schedule', back_populates='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    

class Sched_Workout(db.Model):
    '''A scheduled workout.'''

    __tablename__ = 'sched_workouts'

    schedule_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=False)
    sched_date = db.Column(db.Date, nullable=False)
    sched_order = db.Column(db.Integer, nullable=False)
    discipline = db.Column(db.String, nullable=False)
    workout_id = db.Column(db.String, 
                           db.ForeignKey('workouts.workout_id'))
    # completed = db.Column(db.Boolean)
    completed_id = db.Column(db.String)

    user = db.relationship('User', back_populates='sched_workouts')
    workout = db.relationship('Workout', back_populates='sched_workouts')

    def __repr__(self):
        return (f'<Sched_Workout user_id={self.user_id} ' 
                f'sched_date={self.sched_date} '
                f'sched_order={self.sched_order}>')


class Workout(db.Model):
    '''A workout.'''

    __tablename__ = 'workouts'

    workout_id = db.Column(db.String,
                           primary_key=True)
    discipline = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable = False)
    instructor = db.Column(db.String)
    title = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    sched_workouts = db.relationship('Sched_Workout', back_populates='workout')
    
    def __repr__(self):
        return f'<Workout {self.title} with {self.instructor}>'
    

class Schedule(db.Model):
    '''A schedule.'''

    __tablename__ = 'schedules'

    storage_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    creator = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    sched_name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    sched_type = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    workouts = db.Column(db.JSON, nullable=False)

    user = db.relationship('User', back_populates='schedules')
    
    def __repr__(self):
        return f'<Schedule "{self.sched_name}" created by User {self.creator}>'
    

class Instructor(db.Model):
    '''An Instructor.'''

    __tablename__ = 'instructors'

    instructor_id = db.Column(db.String,
                              primary_key=True)
    instructor_name = db.Column(db.String, nullable=False)

    disciplines = db.relationship('Inst_Disc', back_populates='instructors')

    def __repr__(self):
        return f'<Instructor {self.instructor_name}>'


class Inst_Disc(db.Model):
    '''A instructor:discipline pairing.'''

    __tablename__ = 'instructor_disciplines'

    inst_disc_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)
    instructor_id = db.Column(db.String, 
                              db.ForeignKey('instructors.instructor_id'),
                              nullable=False)
    discipline = db.Column(db.String,
                           nullable=False)
    
    instructors = db.relationship('Instructor', back_populates='disciplines')


class Category(db.Model):
    '''A workout category.'''

    __tablename__ = 'categories'

    category_id = db.Column(db.String,
                            primary_key=True)
    category_name = db.Column(db.String, nullable=False)
    discipline = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Category {self.category_name}, {self.discipline}>'



def connect_to_db(flask_app, db_uri='postgresql:///peloplan', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = False
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)

