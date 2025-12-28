from fastapi import APIRouter, Depends
from app.api.v1.preferences.schemas import PreferencesRequest, PreferencesResponse
from app.api.v1.preferences.service import PreferencesService

router = APIRouter()

def get_current_user():
    return "user-123"

@router.post("/", response_model=PreferencesResponse)
async def update_preferences(
    payload: PreferencesRequest,
    user_id: str = Depends(get_current_user),
    service: PreferencesService = Depends()
):
    return await service.update_preferences(user_id, payload)


from fastapi import APIRouter, Depends
from app.core.security import verify_jwt

router = APIRouter(prefix="/notifications")

@router.get("/")
def get_notifications(user=Depends(verify_jwt)):
    return {
        "message": "Notifications retrieved successfully",
        "user_id": user["sub"]
    }
