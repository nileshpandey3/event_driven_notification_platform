"""
Pydantic schema for basic request/response validations for users table
"""

from pydantic import BaseModel, ConfigDict


class UsersCreate(BaseModel):
    """
    Validation model for creating a new user
    """

    user_id: int


class UsersResponse(BaseModel):
    """
    Validation response model after a successful create request
    """

    user_id: int

    model_config = ConfigDict(from_attributes=True)
