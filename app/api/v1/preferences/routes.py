# This is the API layer, connects HTTP requests → service/repository → DynamoDB

from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_current_user, verify_jwt


router = APIRouter(prefix="/preferences", tags=['preferences'], dependencies=[Depends(verify_jwt)])


@router.post("/")
def create_preferences(user=Depends(get_current_user)):
    # TODO: Add the logic for the api
    return "Testing: Successful Create response"

@router.put("/")
def update_preferences(user=Depends(get_current_user)):
    # TODO: Add the logic for the api
    return "Testing: Successful Put response"

@router.get("/")
def get_preferences(user=Depends(get_current_user)):
    # TODO: Add the logic for the api
    return "Testing: Successful get response"

@router.delete("/")
def remove_preferences(user=Depends(get_current_user)):
    # TODO: Add the logic for the api
    return "Testing: Successful Delete response"
