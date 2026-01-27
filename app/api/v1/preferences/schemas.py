"""
Pydantic schema for basic request/response validations
"""

from typing import List, Literal

from pydantic import BaseModel, ConfigDict


class PreferencesCreate(BaseModel):
    """
    Validation model for creating new preference for a user
    """

    preference_type: str
    mandatory: bool = False
    default_channel: Literal["email", "sms", "push"]  # enforce DB enum constraint


class PreferencesResponse(BaseModel):
    """
    Validation response model after a successful create request
    """

    preference_type: str
    mandatory: bool
    default_channel: str

    model_config = ConfigDict(from_attributes=True)


class UserPreferencesResponse(BaseModel):
    """
    Schema to validate the list of preference responses for each user
    """

    user_id: str
    preferences: List[PreferencesResponse]


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
