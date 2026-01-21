"""
Pydantic schema for basic request/response validations
"""

from pydantic import BaseModel


class PreferencesCreate(BaseModel):
    """
    TODO: Write validation
    """
    type: str
    mandatory: bool = False
    default_channel: str


class PreferencesResponse(BaseModel):
    """
    TODO: Write validation
    """
    user_id: str
    type: str
    mandatory: bool
    default_channel: str

    class Config:
        from_attributes = True

class PreferencesUpdate(BaseModel):
    """
    TODO: Write validation
    """
    type: str
    mandatory: bool
    default_channel: str


class LoginRequest(BaseModel):
    """
    Schema to validate the request format for POST /login
    """

    username: str
    password: str
