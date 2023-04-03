# This code sets up a connection to an SQLite database using SQLAlchemy library and defines a session maker and a declarative base object for ORM models

import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Setting up the name of the SQLite database file
# Setting up the base directory of the file
sqlite_database = "../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

# Setting up the URL to connect to the SQLite database
database_url = f'sqlite:///{os.path.join(base_dir, sqlite_database)}'

# Creating an engine object to connect to the database
engine = create_engine(database_url, echo=True)

# Creating a sessionmaker object to handle database sessions
Session = sessionmaker(bind=engine)

# Creating a declarative base object to define ORM models
Base = declarative_base()
