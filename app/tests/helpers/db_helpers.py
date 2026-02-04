"""
Helpers to mock db requirements
"""

from unittest.mock import MagicMock


def override_get_db():
    """
    Return a mocked db session
    """
    mock_db = MagicMock()
    yield mock_db
