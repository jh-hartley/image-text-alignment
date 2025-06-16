import logging
from typing import cast

import backoff

from src.common.logs import setup_logging
from src.common.new_llm.registry import get_provider
from src.config import config

logger = logging.getLogger(__name__)
setup_logging()


class Embedding:
    """Main class for handling embeddings."""

    def __init__(self) -> None:
        provider = config.LLM_PROVIDER.lower()
        logger.debug(f"Initialising embedding provider: {provider}")
        provider_cls = get_provider("embedding", provider)
        self._provider = provider_cls()

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=config.OPENAI_EMBEDDING_MAX_TRIES,
        max_time=config.OPENAI_EMBEDDING_MAX_TIME,
        base=config.OPENAI_EMBEDDING_BACKOFF_BASE,
        jitter=(
            backoff.full_jitter
            if config.OPENAI_EMBEDDING_BACKOFF_JITTER
            else None
        ),
    )
    def embed_text(self, text: str) -> list[float]:
        logger.debug(f"Getting embedding for text: {text[:50]}...")
        return cast(list[float], self._provider.embed_text(text))

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=config.OPENAI_EMBEDDING_MAX_TRIES,
        max_time=config.OPENAI_EMBEDDING_MAX_TIME,
        base=config.OPENAI_EMBEDDING_BACKOFF_BASE,
        jitter=(
            backoff.full_jitter
            if config.OPENAI_EMBEDDING_BACKOFF_JITTER
            else None
        ),
    )
    def embed_image(self, image: bytes) -> list[float]:
        logger.debug("Getting embedding for image")
        return cast(list[float], self._provider.embed_image(image))

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=config.OPENAI_EMBEDDING_MAX_TRIES,
        max_time=config.OPENAI_EMBEDDING_MAX_TIME,
        base=config.OPENAI_EMBEDDING_BACKOFF_BASE,
        jitter=(
            backoff.full_jitter
            if config.OPENAI_EMBEDDING_BACKOFF_JITTER
            else None
        ),
    )
    def embed_multimodal(self, text: str, image: bytes) -> list[float]:
        logger.debug(
            f"Getting multimodal embedding for text: {text[:50]}... and image"
        )
        return cast(list[float], self._provider.embed_multimodal(text, image))

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=config.OPENAI_EMBEDDING_MAX_TRIES,
        max_time=config.OPENAI_EMBEDDING_MAX_TIME,
        base=config.OPENAI_EMBEDDING_BACKOFF_BASE,
        jitter=(
            backoff.full_jitter
            if config.OPENAI_EMBEDDING_BACKOFF_JITTER
            else None
        ),
    )
    async def aembed_text(self, text: str) -> list[float]:
        logger.debug(f"Getting async embedding for text: {text[:50]}...")
        return cast(list[float], await self._provider.aembed_text(text))

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=config.OPENAI_EMBEDDING_MAX_TRIES,
        max_time=config.OPENAI_EMBEDDING_MAX_TIME,
        base=config.OPENAI_EMBEDDING_BACKOFF_BASE,
        jitter=(
            backoff.full_jitter
            if config.OPENAI_EMBEDDING_BACKOFF_JITTER
            else None
        ),
    )
    async def aembed_image(self, image: bytes) -> list[float]:
        logger.debug("Getting async embedding for image")
        return cast(list[float], await self._provider.aembed_image(image))

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=config.OPENAI_EMBEDDING_MAX_TRIES,
        max_time=config.OPENAI_EMBEDDING_MAX_TIME,
        base=config.OPENAI_EMBEDDING_BACKOFF_BASE,
        jitter=(
            backoff.full_jitter
            if config.OPENAI_EMBEDDING_BACKOFF_JITTER
            else None
        ),
    )
    async def aembed_multimodal(self, text: str, image: bytes) -> list[float]:
        logger.debug(
            "Getting async multimodal embedding "
            f"for text: {text[:50]}... and image"
        )
        return cast(
            list[float], await self._provider.aembed_multimodal(text, image)
        )
