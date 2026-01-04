"""
Module to load all the env vars from a local .env file
"""

import os
from dotenv import load_dotenv


load_dotenv()


def required(name: str):
    """
    Make sure the env var exists and are loaded before every session
    """
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


USERNAME = required("TEST_USER")
PASSWORD = required("TEST_PASSWORD")
ALGORITHMS = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = required("SECRET_KEY")
