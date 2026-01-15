"""
Verify auth routes module
"""

from unittest.mock import patch
from fastapi import HTTPException
from fastapi.testclient import TestClient

import pytest

from app.core.auth import get_current_user
from app.core.config import PASSWORD, USERNAME
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

    @pytest.mark.valid_login
    def test_valid_login(self, mock_create_access_token, mock_redis_client):
        """
        Verify that a valid user can log in and receive an auth token
        and the user is set in redis
        """
        mock_create_access_token.return_value = "mocked.jwt.token"

        payload = {"username": USERNAME, "password": PASSWORD}

        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == 200

        body = response.json()
        assert body["message"] == "Auth Login successful"
        assert body["access_token"] == "mocked.jwt.token"
        assert body["token_type"] == "bearer"

        mock_create_access_token.assert_called_once()

        # Verify redis was updated correctly
        mock_redis_client.set.assert_called_once()
        args, kwargs = mock_redis_client.set.call_args

        assert args[0].startswith("user:")
        assert args[1] == "mocked.jwt.token"
        assert kwargs["ex"] == 3600

    @pytest.mark.invalid_credentials
    def test_invalid_credentials(self, mock_create_access_token, mock_redis_client):
        """
        Verify that invalid user can't log in and receive an auth token
        """
        mock_create_access_token.return_value = "mocked.jwt.token"

        payload = {"username": "invalid_user", "password": "random_password"}

        response = client.post("/api/v1/auth/login", json=payload)
        assert response.status_code == 401
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
        assert response.status_code == 200
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
            raise HTTPException(status_code=401)

        app.dependency_overrides[get_current_user] = invalid_user
        response = client.post("/api/v1/auth/logout")

        assert response.status_code == 401

        mock_redis_client.delete.assert_not_called()
        mock_create_access_token.assert_not_called()

    @classmethod
    def teardown_class(cls):
        """
        Run at the end of all tests
        """
        app.dependency_overrides.clear()
