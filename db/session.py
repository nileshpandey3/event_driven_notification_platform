"""
Module to create and manage a postgres db session
"""

from sqlalchemy.orm import sessionmaker
from db.engine import engine

session = sessionmaker(bind=engine)


def get_db():
    """
    Create a new db session and manage its lifecycle
    """
    db = session()
    try:
        yield db
    finally:
        db.close()
