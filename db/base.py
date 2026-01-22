"""
Declarative Base class for SQL Alchemy
"""

from sqlalchemy.orm import DeclarativeBase

# pylint: disable=too-few-public-methods


class Base(DeclarativeBase):
    """
    This is a framework base class
    Docs: https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html
    """
