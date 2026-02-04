"""
Helpers to mock test function requirements
"""

from app.core.config import USERNAME


def override_get_current_user():
    """
    Return a mocked authenticated user
    required to make requests to protected endpoints
    """
    return USERNAME
