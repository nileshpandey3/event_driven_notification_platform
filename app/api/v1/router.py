from urllib.parse import urlencode
from fastapi import FastAPI, Request

import requests
from fastapi import APIRouter
from starlette.responses import RedirectResponse

from app.api.v1.preferences.routes import router as preferences_router
from app.core.config import AUTH0_AUDIENCE, AUTH0_CLIENT_ID, AUTH0_DOMAIN, REDIRECT_URI, AUTH0_CLIENT_SECRET

router = APIRouter()

router.include_router(preferences_router, prefix="/preferences", tags=["Preferences"])


@router.get("/test")
def test():
    return {"message": "API v1 working!"}

@router.get("/login")
def login():
    params = {
        "audience": AUTH0_AUDIENCE,
        "scope": "openid profile email",
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
    }
    url = f"https://{AUTH0_DOMAIN}/authorize?" + urlencode(params)
    return RedirectResponse(url)

@router.get("/auth/callback")
def auth_callback(request: Request):
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
    print(tokens)
    return tokens