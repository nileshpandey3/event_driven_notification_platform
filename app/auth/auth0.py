import requests
from fastapi import HTTPException
from app.core.config import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_AUDIENCE
)

def login_with_password(username: str, password: str):
    url = f"https://{AUTH0_DOMAIN}/oauth/token"

    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "audience": AUTH0_AUDIENCE,
        "scope": "openid profile email",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET
    }

    resp = requests.post(url, json=payload)

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail=resp.json())

    return resp.json()
