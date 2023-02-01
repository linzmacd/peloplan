import os
import model
import server


# CAN BE USED TO INITIATE OR RESET DATABASE

os.system('dropdb peloplan')
os.system('createdb peloplan')

model.connect_to_db(server.app)
model.db.create_all()