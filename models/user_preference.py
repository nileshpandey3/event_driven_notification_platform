"""
SQLAlchemy ORM model for the User preferences table
"""

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    func,
    ForeignKey,
    BIGINT,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from db.base import Base

# pylint: disable=too-few-public-methods
# pylint: disable=not-callable

class Users(Base):
    """
    Since one user can have multiple preferences we create a Users table to
    store each unique users
    """

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


class UserPreferences(Base):
    """
    Table to store multiple rows of preference types and their associated
    properties like 'mandatory', 'default_channel' etc. for each user
    """

    __tablename__ = "user_preferences"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    preference_type = Column(String, nullable=False)
    mandatory = Column(Boolean, nullable=False, default=False)

    # To ensure that we don't allow unwanted default channel e.g. fax
    # We will enforce a channel enum to enforce DB level validation
    ChannelEnum = ENUM(
        "email",
        "sms",
        "push",
        name="channel_enum",
    )
    default_channel = Column(ChannelEnum, nullable=False)

    # Additional table columns to make queries easier at scale
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("Users", back_populates="preferences")

    # To ensure we don't allow duplicate preference_type for the same user
    # we will enforce unique constraints
    __table_args__ = (
        UniqueConstraint("user_id", "preference_type", name="uq_user_preference"),
    )
