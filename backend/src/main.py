from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger

from core.config import settings
from db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for FastAPI application."""
    logger.info("Application startup completed")
    yield

    await engine.dispose()
    logger.info("Application shutdown completed")


app: FastAPI = FastAPI(
    title="Spy Cat Agency Management API",
    description="CRUD API for managing spy cats, missions, and targets",
    debug=settings.debug,
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")
