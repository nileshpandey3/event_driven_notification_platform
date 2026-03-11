"""
Verify users routes module
"""

from http import HTTPStatus
from unittest.mock import patch

from fastapi.testclient import TestClient

import pytest

from app.core.auth import get_current_user, require_admin
from app.tests.helpers.auth_helpers import (
    override_get_current_user,
    override_require_admin,
)
from app.tests.helpers.db_helpers import override_get_db
from db.session import get_db
from main import app

client = TestClient(app)


@patch("app.api.v1.users.routes.add_user")
@pytest.mark.users_routes
class TestUsersRoutes:
    """
    Verify test cases for users routes module which handles
    adding new users to the db
    """

    @classmethod
    def setup_class(cls):
        """
        Setup mocking requirements for the /users endpoint
        """
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db

    @pytest.mark.add_user
    def test_add_user(self, mock_add_user):
        """
        Verify that a new user can be added to the
        users table
        """

        user = {"username": "test_user_1", "password": "test_password@123"}
        mock_add_user.return_value = {"user_id": "2", "username": user["username"]}

        response = client.post("/api/v1/users/", json=user)

        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        assert isinstance(body["user_id"], int)

    @classmethod
    def teardown_class(cls):
        """
        Run at the end of all tests
        """
        app.dependency_overrides.clear()


@pytest.mark.delete_users
class TestDeleteUsers:
    """
    Test class to verify delete user scenarios
    by both admin and non-admin roles
    """

    @classmethod
    def setup_class(cls):
        """
        Setup dependencies to verify DELETE /users
        endpoint
        """
        app.dependency_overrides[get_db] = override_get_db

    @pytest.mark.delete_user_by_non_admin
    def test_delete_user_by_non_admin(self):
        """
        Verify that if a user doesn't have authorization
        as an admin then they cant perform user deletion
        """

        app.dependency_overrides[get_current_user] = override_get_current_user

        user_id = 4
        response = client.delete(f"/api/v1/users/{user_id}")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json()["detail"] == "Admin privileges required"

    @pytest.mark.delete_user_by_admin
    def test_delete_user_by_admin(self):
        """
        Verify that an authorized admin user
        can delete a user from the db
        """

        # Mock admin dependency
        app.dependency_overrides[require_admin] = override_require_admin

        user_id = 3
        response = client.delete(f"/api/v1/users/{user_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json()["message"] == "User deleted successfully"

        # Clean up admin dependency to not affect other tests
        app.dependency_overrides.pop(require_admin, None)

    @classmethod
    def teardown_class(cls):
        """
        Run at the end of all tests
        """
        app.dependency_overrides.clear()
