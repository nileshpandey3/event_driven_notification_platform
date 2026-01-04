"""
Integration tests for /preferences endpoint
"""

import pytest


@pytest.mark.preference_api
class TestPreferenceApi:
    """
    Test class to verify CRUD /preference API endpoints
    """

    @classmethod
    def setup_class(cls):
        """
        TODO: write test setup
        """

    @pytest.mark.create
    def test_create(self):
        """
        TODO: Write test logic
        """

    @pytest.mark.read
    def test_read(self):
        """
        TODO: Write test logic
        """

    @pytest.mark.update
    def test_update(self):
        """
        TODO: Write test logic
        """

    @pytest.mark.delete
    def test_delete(self):
        """
        TODO: Write test logic
        """

    @classmethod
    def teardown_class(cls):
        """
        TODO: teardown the setup
        """
