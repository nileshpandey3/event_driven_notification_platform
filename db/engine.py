"""
Create a new postgres DB engine
"""

from sqlalchemy import create_engine

from app.core.config import DATABASE_URL, TEST_DATABASE_URL

engine = create_engine(url=DATABASE_URL)
test_engine = create_engine(url=TEST_DATABASE_URL)
