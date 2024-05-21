from fastapi import FastAPI
from src.routes.user import user
from middleware import DBSessionMiddleware
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

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

    app.add_middleware(DBSessionMiddleware)

    origins = [
        "http://localhost:5173",
    ]


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()