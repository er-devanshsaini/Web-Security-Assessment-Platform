from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health
from app.api.routes import scans
from app.core.config import settings
from app.database.session import create_database_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Run startup work before the API begins handling requests."""
    create_database_tables()
    yield


def create_app() -> FastAPI:
    """Create the FastAPI application and attach routes."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="API for running web security checks and storing scan results.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api")
    app.include_router(scans.router, prefix="/api")

    return app


app = create_app()
