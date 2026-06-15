from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return basic application status for uptime checks."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }
