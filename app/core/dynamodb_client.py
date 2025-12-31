import boto3
from app.core.config import AWS_REGION

_dynamodb = None

def get_dynamodb_resource():
    # Create a single dynamodb resource which runs only once per process and reused everywhere
    global _dynamodb
    if not _dynamodb:
        _dynamodb = boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
        )
    return _dynamodb

"""
app/
    api/
        v1/
            preferences/
                models.py
                repository.py
                routes.py
                schemas.py
                service.py
"""