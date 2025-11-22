# sqlite database setup and shared Base for all sqlalchemy models
# source: i used chatgpt to recall declarative_base + sessionmaker pattern
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# make path for database file "medora.db" inside backend folder
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "medora.db")

# sqlite url (using full path)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# create sqlalchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # sqlite requirement
)

# Base = parent class for all ORM tables
Base = declarative_base()

# factory that creates db sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """open new db session safely"""
    return SessionLocal()