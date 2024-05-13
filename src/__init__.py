from fastapi import FastAPI
from src.routes.user import user
from contextlib import asynccontextmanager

# lifespan code

def create_app():
    app = FastAPI(
        description="This is the REST API for DVote",
        title="DVote API",
        openapi_tags=[{
        "name": "users",
        "description": "Operaciones CRUD de usuarios"
        }]
    )

    app.include_router(user)

    return app

app = create_app()