from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dto.image_processing import ImageProcessingResponse
from src.common.db import get_db
from src.common.llm import Llm
from src.core.image_text_alignment.repositories import (
    ProductOverviewRepository,
)
from src.core.image_text_alignment.service import ImageTextAlignmentService


def image_processing_router() -> APIRouter:
    router = APIRouter(prefix="/image-processing", tags=["image-processing"])

    @router.post(
        "/predict/{product_key}", response_model=ImageProcessingResponse
    )
    async def check_colour_matches_description(
        product_key: str, db: Session = Depends(get_db)
    ) -> ImageProcessingResponse:
        llm = Llm()
        service = ImageTextAlignmentService(
            product_overview_repo=ProductOverviewRepository(session=db),
            llm=llm,
        )
        predictions = await service.check_images_for_products([product_key])
        return ImageProcessingResponse(predictions=predictions)

    return router
