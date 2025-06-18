import logging
from abc import ABC, abstractmethod

from src.common.logging import setup_logging

logger = logging.getLogger(__name__)
setup_logging()


class BaseImageProcessor(ABC):
    """
    Base class for image processors that handle encoding
    images for different LLM providers.
    """

    @abstractmethod
    def encode_image(self, image_bytes: bytes) -> str:
        """Encode image bytes into a format suitable for the LLM provider."""
        raise NotImplementedError("Subclasses must implement this method")
