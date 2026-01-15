from unittest.mock import patch

import ipdb
import pytest
from fastapi.testclient import TestClient

from app.core.config import PASSWORD, USERNAME
from main import app

client = TestClient(app)



@patch("app.api.v1.auth.routes.redis_client")
@patch("app.api.v1.auth.routes.create_access_token")
@pytest.mark.routes
class TestRoutes:

    @pytest.mark.login
    def test_login(self,mock_create_access_token,mock_redis_client):

        # Arrange
        mock_create_access_token.return_value = "mocked.jwt.token"

        payload = {
            "username": USERNAME,
            "password": PASSWORD
        }

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