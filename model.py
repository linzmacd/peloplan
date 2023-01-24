"""Models for PeloPlan app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True )
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    session_id = db.Column(db.String)

    sched_workouts = db.relationship('Sched_Workout', back_populates='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    

class Sched_Workout(db.Model):
    """A scheduled workout."""

    __tablename__ = 'sched_workouts'

    schedule_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True )
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=False)
    sched_date = db.Column(db.Date, nullable=False)
    sched_order = db.Column(db.Integer, nullable=False)
    discipline = db.Column(db.String, nullable=False)
    workout_id = db.Column(db.String, 
                           db.ForeignKey('workouts.workout_id'))

    user = db.relationship('User', back_populates='sched_workouts')
    workout = db.relationship('Workout', back_populates='sched_workouts')

    def __repr__(self):
        return (f'<Sched_Workout user_id={self.user_id}, ' 
                f'sched_date={self.sched_date}, '
                f'sched_order={self.sched_order}>')


class Workout(db.Model):
    """A workout."""

    __tablename__ = 'workouts'

    workout_id = db.Column(db.String,
                           primary_key=True)
    discipline = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable = False)
    instructor = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    sched_workouts = db.relationship('Sched_Workout', back_populates='workout')
    
    def __repr__(self):
        return f'<Workout {self.title} with {self.instructor}>'


def reset_db(): ########## FOR TESTING #################
    '''Seed DB'''
    test_user = User(email='test@test.com', 
                     password='testpw')
    test_workout = Workout(workout_id='fs98sdfs', discipline='cycling', 
                           category='warm up', instructor='sam yo', 
                           title='30 min Rock Ride', duration=900)
    test_sched = Sched_Workout(user_id=1, sched_date='10-07-2023', 
                               sched_order=1, discipline='cycling', 
                               workout_id='fs98sdfs')

    db.session.add(test_user)
    db.session.add(test_workout)
    db.session.add(test_sched)
    db.session.commit()


def connect_to_db(flask_app, db_uri="postgresql:///peloplan", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app, echo=False)

