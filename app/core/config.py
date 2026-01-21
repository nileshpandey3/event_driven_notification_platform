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

POSTGRES_USER=required("POSTGRES_USER")
POSTGRES_PASSWORD=required("POSTGRES_PASSWORD")
POSTGRES_DB=required("POSTGRES_DB")
POSTGRES_HOST=required("POSTGRES_HOST")
POSTGRES_PORT=required("POSTGRES_PORT")
DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/{POSTGRES_DB}"
)

