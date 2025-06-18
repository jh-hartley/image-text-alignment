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
    is_mismatch: bool
    justification: str
    image_path: str | None = None
    description_synthesis: str
    image_summary: str
