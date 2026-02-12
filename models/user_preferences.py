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

# pylint: disable=not-callable


class UserPreferences(Base):
    """
    Table to store multiple rows of preference types and their associated
    properties like 'mandatory', 'default_channel' etc. for each user
    """

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return self.__class__.__name__

    __tablename__ = "user_preferences"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(
        BIGINT, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    preference_type = Column(String, nullable=False)
    mandatory = Column(Boolean, nullable=False, default=False)

    # To ensure that we don't allow unwanted default channel e.g. fax
    # We will enforce a channel enum to enforce DB level validation
    ChannelEnum = ENUM(
        "email",
        "sms",
        "push",
        name="channel_enum",
        create_type=False,
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
