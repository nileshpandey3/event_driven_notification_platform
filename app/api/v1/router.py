"""
Module to aggregate all different API routes
"""

from fastapi import APIRouter

from app.api.v1.preferences.routes import router as preferences_router
from app.api.v1.auth.routes import router as auth_router

router = APIRouter()

router.include_router(preferences_router)
router.include_router(auth_router)
