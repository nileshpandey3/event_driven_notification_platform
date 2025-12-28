import requests
from app.core.config import AUTH0_AUDIENCE, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, USERNAME, PASSWORD
data = {
    "grant_type": "password",
    "username": USERNAME,
    "password": PASSWORD,
    "audience": AUTH0_AUDIENCE,
    "scope": "openid profile email",
    "client_id": AUTH0_CLIENT_ID,
    "client_secret": AUTH0_CLIENT_SECRET,
    "connection": "Username-Password-Authentication"
}

response = requests.post(f"https://{AUTH0_DOMAIN}/oauth/token", json=data)
tokens = response.json()
print(response.status_code)
print(tokens)
print(response.text)
print("Access Token:", tokens["access_token"])
print("ID Token:", tokens.get("id_token"))
