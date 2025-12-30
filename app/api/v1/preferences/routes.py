from fastapi import APIRouter, Depends

from app.core.auth import get_current_user, verify_jwt


router = APIRouter(prefix="/preferences", tags=['preferences'], dependencies=[Depends(verify_jwt)])

@router.get("/")
def get_preferences(user=Depends(get_current_user)):
    print({
        "message": "test preferences",
        "user_id": user["sub"]
    })
