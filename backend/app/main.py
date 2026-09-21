from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app import models
from backend.app.database import Base, engine
from backend.app.routers import (
    alerts,
    api_keys,
    auth,
    events,
    external,
    incidents,
    response_actions,
    users,
)

Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="ChiSoSecure API",
    description=(
        "Cloud-native security detection and "
        "automated incident response platform."
    ),
    version="0.8.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router
)

app.include_router(
    users.router
)

app.include_router(
    events.router
)

app.include_router(
    api_keys.router
)

app.include_router(
    alerts.router
)

app.include_router(
    incidents.router
)

app.include_router(
    response_actions.router
)

app.include_router(
    external.router
)


@app.get(
    "/",
    tags=["System"]
)
def root():
    return {
        "service": "ChiSoSecure",
        "status": "operational",
        "version": "0.8.0"
    }


@app.get(
    "/health",
    tags=["System"]
)
def health():
    return {
        "status": "healthy"
    }