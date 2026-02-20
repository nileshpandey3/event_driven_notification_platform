"""
Model package initializer.

This module exposes the primary SQLAlchemy ORM models so they can be
imported directly from the `models` package:

    from models import Users, UserPreferences

The `__all__` variable defines the public interface of this package
and ensures only intended models are exported when using
`from models import *`.

Keeping imports centralized here also helps ensure that all models are
loaded for metadata discovery (e.g., Alembic migrations).
"""

from .users import Users
from .user_preferences import UserPreferences

__all__ = ["Users", "UserPreferences"]
