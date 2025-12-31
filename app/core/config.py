from dotenv import load_dotenv
import os

load_dotenv()

def required(name: str):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value

AUTH0_DOMAIN = required("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = required("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = required("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = required("AUTH0_AUDIENCE")
USERNAME=required("AUTH0_USER")
PASSWORD=required("AUTH0_PASSWORD")
ALGORITHMS = ["RS256"]
REDIRECT_URI = required("REDIRECT_URI")
AWS_REGION='us-east-1'
