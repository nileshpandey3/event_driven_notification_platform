import boto3
from app.core.config import AWS_REGION

_dynamodb = None

def get_dynamodb_resource():
    global _dynamodb
    if not _dynamodb:
        _dynamodb = boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
        )
    return _dynamodb

def get_notifications_table():
    return get_dynamodb_resource().Table(settings.DDB_TABLE_NAME)
