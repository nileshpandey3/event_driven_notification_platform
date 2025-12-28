from fastapi import APIRouter, HTTPException, Header
import jwt
import requests

from app.core.config import AUTH0_DOMAIN, AUTH0_AUDIENCE, ALGORITHMS
from app.auth.auth0 import login_with_password

router = APIRouter(prefix="/auth")

jwks = requests.get(
    f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
).json()

def verify_jwt(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.replace("Bearer ", "")

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = None
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if not rsa_key:
        raise HTTPException(status_code=401, detail="Invalid token")

    payload = jwt.decode(
        token,
        rsa_key,
        algorithms=ALGORITHMS,
        audience=AUTH0_AUDIENCE,
        issuer=f"https://{AUTH0_DOMAIN}/"
    )

    return payload

@router.post("/login")
def login(username: str, password: str):
    tokens = login_with_password(username, password)
    return {
        "access_token": tokens["access_token"],
        "expires_in": tokens["expires_in"],
        "token_type": tokens["token_type"]
    }
