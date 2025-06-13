import logging

from src.common.logs import setup_logging
from src.common.new_llm.base_classes import (
    BaseImageProcessor,
)
from src.common.new_llm.registry import get_provider
from src.config import config

logger = logging.getLogger(__name__)
setup_logging()


def get_processor() -> BaseImageProcessor:
    """
    Get the appropriate image processor based on the configured LLM provider.
    """
    provider = config.LLM_PROVIDER.lower()
    logger.debug(f"Getting image processor for provider: {provider}")
    processor_cls = get_provider("image_processor", provider)
    return processor_cls()
