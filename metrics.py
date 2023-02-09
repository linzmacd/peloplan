from flask import session
from model import connect_to_db, db
import pandas as pd

df = pd.read_sql('select * from comp_workouts', db.make_connector)
print(df)



if __name__ == '__main__':
    from server import app
    connect_to_db(app)