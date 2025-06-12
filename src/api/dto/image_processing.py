from pydantic import BaseModel


class ImageProcessingResponse(BaseModel):
    """Placeholder response model for LLM return object."""

    prediction: bool
