"""
SQLAlchemy ORM Model for the Users table
"""

from sqlalchemy import (
    Column,
    DateTime,
    func,
    BIGINT,
)
from sqlalchemy.orm import relationship

from db.base import Base


# pylint: disable=not-callable
class Users(Base):
    """
    Since one user can have multiple preferences we create a Users table to
    store each unique users
    """

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return self.__class__.__name__

    __tablename__ = "users"
    user_id = Column(BIGINT, primary_key=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # cascade==all ensures preferences are deleted if user is deleted.
    # By creating a relationship between these 2 classes we can have a 2 way reference between them,
    # and they can access each other's attributes
    preferences = relationship(
        "UserPreferences", back_populates="user", cascade="all, delete-orphan"
    )
