from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProductImageCheckInput(BaseModel):
    product_key: str
    description: str
    image: str


class ProductImageCheckLLMResponse(BaseModel):
    """Used for parsing LLM output only."""

    is_mismatch: bool
    justification: str
    description_synthesis: str
    image_summary: str


class ProductImageCheckResult(BaseModel):
    product_key: str
    image_path: str | None = None
    is_mismatch: bool
    justification: str
    description_synthesis: str
    image_summary: str


class ImagePredictionDTO(BaseModel):
    batch_key: UUID
    product_key: UUID
    image_path: str | None
    is_mismatch: bool
    justification: str | None
    description_synthesis: str | None
    image_summary: str | None
    created_at: datetime
    updated_at: datetime
