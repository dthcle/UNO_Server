import os
from CONST import RSA_DEPOSITORY_LOCATION
from Entity import Database

"""
when you run the server first time
please run this script
to init the database
"""

if os.path.exists(RSA_DEPOSITORY_LOCATION):
    os.mkdir(RSA_DEPOSITORY_LOCATION)

database = Database()
database.init_database()
database.create_user('admin', 'admin')

