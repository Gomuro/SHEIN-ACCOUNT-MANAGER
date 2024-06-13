import os

from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SQLite database file path
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'vacancies.db')

# SQLAlchemy's declarative base
Base = declarative_base()


# Define a class for vacancy history
datetime_pattern = '%Y-%m-%d %H:%M:%S'
class VacancyHistory(Base):
    __tablename__ = 'vacancy_history'

    id = Column(Integer, primary_key=True, index=True)
    query_time = Column(DateTime)
    vacancy_count = Column(Integer)
    change = Column(Integer)


# Create an engine to connect to the SQLite database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create all tables in the database (if they do not exist)
Base.metadata.create_all(bind=engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
