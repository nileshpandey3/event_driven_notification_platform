"""
Declarative Base class for SQL Alchemy
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    This is a framework base class
    Docs: https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html
    """

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return self.__class__.__name__
