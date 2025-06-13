from abc import ABC, abstractmethod

import backoff

from src.config import config


class BaseEmbeddingProvider(ABC):
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
    @abstractmethod
    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError(
            "aembed_documents has not been defined for this class."
        )
