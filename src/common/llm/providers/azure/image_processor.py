import base64
import logging

from src.common.llm.base_classes import BaseImageProcessor
from src.common.llm.registry import register_provider
from src.common.logging import setup_logging

from .constants import PROVIDER

logger = logging.getLogger(__name__)
setup_logging()


@register_provider("image_processor", PROVIDER)
class AzureImageProcessor(BaseImageProcessor):
    """Image processor for Azure OpenAI's API format."""

    def encode_image(self, image_bytes: bytes) -> str:
        """Encode image bytes as a base64 data URL for Azure OpenAI's API."""
        logger.debug("Encoding image for Azure provider")
        return (
            f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode()}"
        )
