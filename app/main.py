from fastapi import FastAPI

app = FastAPI(title="Notification Service")

app.include_router()