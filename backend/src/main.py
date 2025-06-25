from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.config import settings

app: FastAPI = FastAPI(
    title="Spy Cat Agency Management API",
    description="CRUD API for managing spy cats, missions, and targets",
    debug=settings.debug,
)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")
