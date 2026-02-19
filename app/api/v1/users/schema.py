"""
Pydantic schema for basic request/response validations for users table
"""

from pydantic import BaseModel, ConfigDict, Field


class UsersCreate(BaseModel):
    """
    Validation model for creating a new user
    using a username and password
    """

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=3, max_length=50)


class UsersResponse(BaseModel):
    """
    Validation response model after a successful create request
    """

    user_id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
