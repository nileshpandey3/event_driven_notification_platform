"""
Pydantic schema for basic request/response validations
"""

from typing import List, Literal

from pydantic import BaseModel


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

    class Config: # pylint: disable=too-few-public-methods
        """
        Since FAstAPI returns ORM objects with attributes e.g. 'obj.preference_type'
        and pydantic expects dicts, this class will instruct pydantic to
        read values from those attributes instead of expecting a dict.
        """
        from_attributes = True


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
