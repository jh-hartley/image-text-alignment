from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dto.image_processing import ImageProcessingResponse
from src.common.db import get_db
from src.core.image_text_alignment.service import (
    CheckImageTextAlignmentService,
)


def image_processing_router() -> APIRouter:
    router = APIRouter(prefix="/image-processing", tags=["image-processing"])

    @router.post(
        "/predict/{product_key}", response_model=ImageProcessingResponse
    )
    async def check_colour_matches_description(
        product_key: str, db: Session = Depends(get_db)
    ) -> ImageProcessingResponse:
        service = CheckImageTextAlignmentService.from_session(db)
        prediction = await service.check_colour_matches_description(
            product_key
        )
        return ImageProcessingResponse(prediction=prediction)

    return router
