from pydantic import BaseModel

from src.core.image_text_alignment.dtos import ProductImageCheckResult


class ImageProcessingResponse(BaseModel):
    predictions: list[ProductImageCheckResult]
