"""
SQLAlchemy ORM model for the User preferences table
"""
from sqlalchemy import Column, String, Boolean, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class Users(Base):
    """
    Since one user can have multiple preferences we create a Users table to
    store each unique users
    """
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)

    # cascade all ensures preferences are deleted if user is deleted.
    # By creating a relationship between these 2 classes we can have a 2 way reference between them,
    # and they can access each other's attributes
    preferences = relationship("UserPreferences", back_populates="user", cascade="all, delete-orphan")

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    preference_type = Column(String)
    mandatory = Column(Boolean, nullable=False, default=False)
    default_channel = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    user = relationship("Users", back_populates="preferences")

