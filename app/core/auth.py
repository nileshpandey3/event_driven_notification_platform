from fastapi import Depends
from fastapi import Header, HTTPException
from jose import jwt, jwk, JWTError

from app.core.config import AUTH0_AUDIENCE
import jwt
import requests
from app.core.config import AUTH0_DOMAIN, ALGORITHMS




def get_rsa_key(kid: str):
    """
    Fetch the JWKS from Auth0 and return the RSA key matching the kid
    """
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    for key in jwks["keys"]:
        if key["kid"] == kid:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    return None

def verify_jwt(authorization: str = Header(...)):
    """
    Verifies the JWT from the Authorization header.
    Returns the decoded payload if valid.
    Raises HTTPException if invalid.
    """

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    # Decode header to get kid
    try:
        # Extract kid from token header
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = get_rsa_key(unverified_header.get("kid"))

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Unable to find appropriate key")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(rsa_key)


        # Decode token WITHOUT audience first
        payload = jwt.decode(
            token,
            public_key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )

    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Unable to parse authentication token")

    return payload


def get_current_user(payload=Depends(verify_jwt)):
    return payload
