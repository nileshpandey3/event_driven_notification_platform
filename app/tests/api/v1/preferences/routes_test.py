"""
Module to test /preferences routes test cases
"""

from http import HTTPStatus
from unittest.mock import patch

import ipdb
import pytest

from fastapi.testclient import TestClient
from app.core.auth import get_current_user
from app.tests.api.v1.auth.routes_test import client
from app.tests.helpers.auth_helpers import override_get_current_user
from app.tests.helpers.db_helpers import override_get_db
from db.session import get_db
from main import app

client = TestClient(app)


def _get_current_user_returns_id():
    return "1"


@patch("app.api.v1.preferences.routes.get_user_preferences")
@pytest.mark.get_user_preferences
class TestGetUserPreferences:
    @classmethod
    def setup_class(cls):
        app.dependency_overrides[get_current_user] = _get_current_user_returns_id
        app.dependency_overrides[get_db] = override_get_db

        cls.expected_preferences = [
            {
                "preference_type": "password_reset",
                "mandatory": True,
                "default_channel": "email",
            },
            {
                "preference_type": "marketing",
                "mandatory": False,
                "default_channel": "sms",
            },
        ]

    @pytest.mark.get_preferences_returns_list
    def test_get_preferences_returns_list(self, mock_get_user_preferences):
        mock_get_user_preferences.return_value = self.expected_preferences

        response = client.get("api/v1/preferences/")
        response.raise_for_status()
        body = response.json()

        assert response.status_code == HTTPStatus.OK
        assert isinstance(body, list)
        assert len(body) == 2
        assert body[0]["preference_type"] == "password_reset"
        assert body[0]["mandatory"] is True
        assert body[0]["default_channel"] == "email"
        assert body[1]["preference_type"] == "marketing"
        assert body[1]["mandatory"] is False
        assert body[1]["default_channel"] == "sms"
        mock_get_user_preferences.assert_called_once()
        call_args = mock_get_user_preferences.call_args
        assert call_args[0][0] == 1
        assert call_args[0][1] is not None

    @pytest.mark.get_preferences_returns_empty_list
    def test_get_preferences_returns_empty_list(self, mock_get_user_preferences):
        mock_get_user_preferences.return_value = []

        response = client.get("api/v1/preferences/")
        response.raise_for_status()
        body = response.json()

        assert response.status_code == HTTPStatus.OK
        assert body == []

    @classmethod
    def teardown_class(cls):
        app.dependency_overrides.clear()


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
        Verify that we can successfully POST a valid users preferences
        """
        mock_add_user_preference.return_value = self.preference_body

        response = client.post("api/v1/preferences/", json=self.preference_body)
        response.raise_for_status()
        body = response.json()

        assert response.status_code == HTTPStatus.CREATED
        assert body["preference_type"] == self.preference_body["preference_type"]
        assert body["mandatory"] == self.preference_body["mandatory"]
        assert body["default_channel"] == self.preference_body["default_channel"]

    @classmethod
    def teardown_class(cls):
        """
        Run at the end of all tests
        """
        app.dependency_overrides.clear()

@patch("app.api.v1.preferences.routes.update_user_preference")
@pytest.mark.update_user_preference
class TestUpdateUserPreferences:

    @classmethod
    def setup_class(cls):
        """
        Setup mocking requirements for the PATCH /{preference_type} endpoint
        """
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db

        # Preferences request payload
        cls.preference_body = {
            "mandatory": True,
            "default_channel": "email",
        }

    @pytest.mark.update_user_preference
    def test_update_user_preferences(self, mock_update_user_preferences):
        preference_type= "subscription_renewal"
        mock_update_user_preferences.return_value = self.preference_body

        response = client.patch(url=f'api/v1/preferences/{preference_type}', json=self.preference_body)
        response.raise_for_status()
        body = response.json()

        assert body['mandatory'] == self.preference_body['mandatory']
        assert body['default_channel'] == self.preference_body['default_channel']

        mock_update_user_preferences.assert_called_once()


    @classmethod
    def teardown_class(cls):
        """
        Run at the end of all tests
        """
        app.dependency_overrides.clear()


@patch("app.api.v1.preferences.routes.remove_user_preference")
@pytest.mark.remove_user_preference
class TestRemoveUserPreference:
    """
    Verify DELETE /{preference_type} endpoint
    """
    @classmethod
    def setup_class(cls):
        """
        Setup mocking requirements for the DELETE /{preference_type} endpoint
        """
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db

    @pytest.mark.remove_user_preference
    def test_remove_user_preference(self, mock_remove_user_preference):
        """
        Verify that we can successfully remove a user's preference
        """
        mock_remove_user_preference.return_value = True
        preference_type = "subscription_renewal"

        response = client.delete(url=f'api/v1/preferences/{preference_type}')

        assert response.status_code == 204
        assert response.text == ""

        mock_remove_user_preference.assert_called_once()

    @classmethod
    def teardown_class(cls):
        """
        Run at the end of all tests
        """
        app.dependency_overrides.clear()

