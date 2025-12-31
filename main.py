from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.core.redis_client import redis_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    # App startup 'uvicorn main:app --reload' and shutdown helper when ctrl+c is used to shut down the app
    print("🚀 Application starting up")
    yield
    print("Shutting down FastApi App")
    redis_client.close()

app = FastAPI(title="Notification Service", lifespan=lifespan)
app.include_router(v1_router, prefix="/api/v1")
