import logging

from src.common.logs import setup_logging
from src.common.new_llm.registry import get_provider
from src.config import config

logger = logging.getLogger(__name__)
setup_logging()


class ImageEncoder:
    """Main class for handling image encoding."""

    def __init__(self) -> None:
        provider = config.LLM_PROVIDER.lower()
        logger.debug(f"Initialising image processor: {provider}")
        processor_cls = get_provider("image_processor", provider)
        self._processor = processor_cls()

    def encode_image(self, image_bytes: bytes) -> str:
        """
        Encode image bytes into the format required by the current provider.
        """
        logger.debug("Encoding image bytes")
        return self._processor.encode_image(image_bytes) # type: ignore
