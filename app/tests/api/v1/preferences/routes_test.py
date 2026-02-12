"""
Module to test /preferences routes test cases
"""

from http import HTTPStatus
from unittest.mock import patch

import pytest

from fastapi.testclient import TestClient
from app.core.auth import get_current_user
from app.tests.api.v1.auth.routes_test import client
from app.tests.helpers.auth_helpers import override_get_current_user
from app.tests.helpers.db_helpers import override_get_db
from db.session import get_db
from main import app

client = TestClient(app)


@patch("app.api.v1.preferences.routes.add_user_preference")
@pytest.mark.users_routes
class TestCreateUserPreferences:
    """
    Class to verify POST '/preferences' endpoint
    """

    @classmethod
    def setup_class(cls):
        """
        Setup mocking requirements for the /preferences endpoint
        """
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db

        # Preferences request payload
        cls.preference_body = {
            "preference_type": "password_reset",
            "mandatory": True,
            "default_channel": "email",
        }

    @pytest.mark.create_user_preferences
    def test_create_user_preferences(self, mock_add_user_preference):
        """
        Verify that we can successfully add preferences for a new user
        using the POST /preferences endpoint
        """
        mock_add_user_preference.return_value = self.preference_body

        response = client.post("api/v1/preferences/", json=self.preference_body)
        response.raise_for_status()
        body = response.json()

        assert response.status_code == HTTPStatus.CREATED
        assert body["preference_type"] == self.preference_body["preference_type"]
        assert body["mandatory"] == self.preference_body["mandatory"]
        assert body["default_channel"] == self.preference_body["default_channel"]


    def test_idempotency(self):
        pass

    @classmethod
    def teardown_class(cls):
        """
        Run at the end of all tests
        """
        app.dependency_overrides.clear()
