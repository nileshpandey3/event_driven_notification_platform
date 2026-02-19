"""
Verify auth routes module
"""

from http import HTTPStatus
from unittest.mock import patch, MagicMock

import ipdb
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

import pytest

from app.core.auth import get_current_user
from app.core.config import PASSWORD, USERNAME
from db.session import get_db
from main import app

client = TestClient(app)


@patch("app.api.v1.auth.routes.redis_client")
@patch("app.api.v1.auth.routes.create_access_token")
@pytest.mark.routes
class TestRoutes:
    """
    Verify test cases for auth routes module which handles
    user authentication for calling the protected api endpoints
    """

    @classmethod
    def setup_class(cls):
        """
        Setup data to be used to verify /login endpoint
        """
        # Configure mock db session to be used by login tests
        cls.mock_db = MagicMock()
        app.dependency_overrides[get_db] = lambda: cls.mock_db

        # Configure a mock valid user object
        cls.user = MagicMock()
        cls.user.user_id = 1
        cls.user.username = "mocked_valid_user"
        cls.user.password = "secret_test_password"

    @pytest.mark.valid_login
    def test_valid_login(self, mock_create_access_token, mock_redis_client):
        """
        Verify that a valid user can log in and receive an auth token
        and the user is set in redis
        """
        mock_create_access_token.return_value = "mocked.jwt.token"

        # Mock the db response for a valid existing user
        self.mock_db.query().filter().first.return_value = self.user

        payload = {"username": "mocked_valid_user", "password": "secret_test_password"}

        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == HTTPStatus.OK

        body = response.json()
        assert body["message"] == "Auth Login successful"
        assert body["access_token"] == "mocked.jwt.token"
        assert body["token_type"] == "bearer"

        mock_create_access_token.assert_called_once()

        # Verify redis was updated correctly
        mock_redis_client.set.assert_called_once()
        args, token_expiry = mock_redis_client.set.call_args

        assert args[0].startswith("user:")
        assert args[1] == "mocked.jwt.token"
        # verify token expiry time is set to 3600 seconds
        assert token_expiry["ex"] == 3600

    @pytest.mark.invalid_credentials
    def test_invalid_credentials(self, mock_authenticate, mock_redis_client):
        """
        Verify that invalid user can't log in and receive an auth token
        """
        mock_authenticate.side_effect = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

        payload = {"username": "invalid_user", "password": "invalid_password"}

        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        detail = response.json()["detail"]
        assert detail == "Invalid Username or Password"

        # Assert that the redis client was not set with the invalid user
        mock_redis_client.set.assert_not_called()

    @pytest.mark.logout_authenticated_user
    def test_logout_authenticated_user(
        self, mock_create_access_token, mock_redis_client
    ):
        """
        Verify that an authenticated user can successfully log out
        """
        app.dependency_overrides[get_current_user] = lambda: "fake_user_id"

        response = client.post("/api/v1/auth/logout")
        assert response.status_code == HTTPStatus.OK
        message = response.json()["message"]

        assert message == "Logged out successfully"

        mock_redis_client.delete.assert_called_once()
        mock_create_access_token.assert_not_called()

    @pytest.mark.non_authenticated_user_logout
    def test_non_authenticated_user_logout(
        self, mock_create_access_token, mock_redis_client
    ):
        """
        Verify that a non-authenticated user can't be logged out
        """

        # simulate a fake/invalid user
        def invalid_user():
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

        app.dependency_overrides[get_current_user] = invalid_user
        response = client.post("/api/v1/auth/logout")

        assert response.status_code == HTTPStatus.UNAUTHORIZED

        mock_redis_client.delete.assert_not_called()
        mock_create_access_token.assert_not_called()

    @classmethod
    def teardown_class(cls):
        """
        Run at the end of all tests
        """
        app.dependency_overrides.clear()
