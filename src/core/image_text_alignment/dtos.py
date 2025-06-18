from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProductImageCheckInput(BaseModel):
    product_key: str
    description: str
    image: str


class ProductImageCheckLLMResponse(BaseModel):
    """Used for parsing LLM output only."""

    attribute_matches_image: str
    description_matches_image: str
    attribute_image_justification: str
    description_image_justification: str
    description_synthesis: str
    image_summary: str


class ProductImageCheckResult(BaseModel):
    product_key: str
    image_path: str | None = None
    attribute_matches_image: str
    description_matches_image: str
    attribute_image_justification: str
    description_image_justification: str
    description_synthesis: str
    image_summary: str


class ImagePredictionDTO(BaseModel):
    batch_key: UUID
    product_key: UUID
    image_name: str | None
    attribute_matches_image: str
    description_matches_image: str
    attribute_image_justification: str | None
    description_image_justification: str | None
    description_synthesis: str | None
    image_summary: str | None
    created_at: datetime
    updated_at: datetime
