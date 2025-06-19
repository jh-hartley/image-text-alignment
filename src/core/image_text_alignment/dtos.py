from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProductImageCheckInput(BaseModel):
    product_key: str
    description: str
    image: str


class ProductImageRefereeInput(BaseModel):
    """Input for the referee, including the classifier's output."""

    product_key: str
    description: str
    image: str
    classifier_colour_status: str
    classifier_colour_justification: str
    classifier_image_summary: str
    classifier_description_synthesis: str


class ProductImageCheckLLMResponse(BaseModel):
    """Used for parsing LLM output only."""

    colour_status: str
    colour_justification: str
    image_summary: str
    description_synthesis: str


class ProductImageRefereeLLMResponse(BaseModel):
    """Used for parsing LLM output only."""

    final_colour_status: str
    final_colour_justification: str


class ProductImageClassificationResult(BaseModel):
    product_key: str
    image_path: str | None
    colour_status: str
    colour_justification: str
    image_summary: str
    description_synthesis: str


class ProductImageRefereeResult(BaseModel):
    final_colour_status: str
    final_colour_justification: str


class ImagePredictionDTO(BaseModel):
    batch_key: UUID
    product_key: UUID
    image_name: str | None
    colour_status: str
    colour_justification: str
    image_summary: str
    description_synthesis: str
    final_colour_status: str
    final_colour_justification: str
    created_at: datetime
    updated_at: datetime
