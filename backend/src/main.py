from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core.config import settings
from db.session import engine
from routers import cat_router, mission_router, target_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for FastAPI application."""
    yield

    await engine.dispose()


app: FastAPI = FastAPI(
    title="Spy Cat Agency Management API",
    description="CRUD API for managing spy cats, missions, and targets",
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    middleware_class=CORSMiddleware,  # type: ignore
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=cat_router, prefix=settings.api_prefix)
app.include_router(router=mission_router, prefix=settings.api_prefix)
app.include_router(router=target_router, prefix=settings.api_prefix)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")
