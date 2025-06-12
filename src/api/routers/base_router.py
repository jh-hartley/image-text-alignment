from fastapi import APIRouter

from src.api.routers.image_processing import image_processing_router


def base_router() -> APIRouter:
    """Create base router with all API routes."""

    router = APIRouter()

    router.include_router(image_processing_router())

    return router
