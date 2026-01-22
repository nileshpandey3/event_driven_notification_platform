"""
Create a new postgres DB engine
"""

from sqlalchemy import create_engine

from app.core.config import DATABASE_URL

engine = create_engine(url=DATABASE_URL)
