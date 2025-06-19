from pydantic import BaseModel

from src.core.image_text_alignment.dtos import ProductImageClassificationResult


class ImageProcessingResponse(BaseModel):
    predictions: list[ProductImageClassificationResult]
