from urllib.parse import urlencode
from fastapi import Request, APIRouter, Depends

import requests
from jose import jwt
from starlette.responses import RedirectResponse

from app.core.config import (AUTH0_AUDIENCE, AUTH0_CLIENT_ID, AUTH0_DOMAIN,
                             REDIRECT_URI, AUTH0_CLIENT_SECRET)
from app.core.redis_client import redis_client
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/login")
def login():
    """
    Authenticating the user by redirecting the user to AUTH0 Identity Provider
    """
    params = {
        "audience": AUTH0_AUDIENCE,
        "scope": "openid profile email",
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
    }
    url = f"https://{AUTH0_DOMAIN}/authorize?" + urlencode(params)
    return RedirectResponse(url)

@router.get("/callback")
def auth_callback(request: Request):
    """
    Exchange the authorization Code received from the auth login for access(Bearer) tokens.
    """
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code provided"}

    # Exchange code for tokens
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(token_url, json=data)
    tokens = response.json()
    access_token = tokens.get("access_token")
    id_token = tokens.get("id_token")

    # We need user_id as a key in the redis store
    payload = jwt.get_unverified_claims(id_token)
    user_id = payload["sub"]

    # Store access_token in Redis with TTL 1 hour
    redis_client.set(f"user:{user_id}:access_token", access_token, ex=3600)
    print(access_token)
    return {"message": "Auth Login successful"}

@router.post("/logout")
def logout(user_id: str = Depends(get_current_user)):
    # Logout and clear the client session
    redis_client.delete(f"session:{user_id}")
    return {"message": "Logged out successfully"}
