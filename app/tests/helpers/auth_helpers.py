"""
Helpers to mock test function requirements
"""

from models import Users


def override_get_current_user():
    """
    Return a mocked authenticated user
    required to make requests to protected endpoints
    """
    # Configure a mock valid user
    return Users(
        user_id=1, username="test_user@example.com", password="secret_password"
    )
