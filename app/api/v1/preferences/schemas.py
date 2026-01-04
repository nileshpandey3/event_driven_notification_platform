"""
Pydantic schema for basic request/response validations
"""

from pydantic import BaseModel


class PreferencesBase(BaseModel):
    """
    TODO: Write validation
    """


class PreferencesCreate(BaseModel):
    """
    TODO: Write validation
    """


class PreferencesUpdate(BaseModel):
    """
    TODO: Write validation
    """


class LoginRequest(BaseModel):
    """
    Schema to validate the request format for POST /login
    """

    username: str
    password: str
