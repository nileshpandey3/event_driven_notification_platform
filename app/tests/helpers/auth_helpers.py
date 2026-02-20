"""
Helpers to mock test function requirements
"""
from unittest.mock import MagicMock

from app.core.config import USERNAME


def override_get_current_user():
    """
    Return a mocked authenticated user
    required to make requests to protected endpoints
    """
    # Configure a mock valid user
    user = MagicMock()
    user.user_id = 1
    return user
