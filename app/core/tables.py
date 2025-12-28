from fastapi import Depends
from app.core.dynamodb_client import get_dynamodb_resource

def get_preferences_table(
    dynamodb=Depends(get_dynamodb_resource)
):
    return dynamodb.Table("user_preferences")
