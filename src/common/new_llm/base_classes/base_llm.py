from abc import ABC, abstractmethod
from typing import TypeVar

import backoff
from pydantic import BaseModel

from src.config import config

T = TypeVar("T", bound=BaseModel)


class BaseLlmProvider(ABC):
    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=config.OPENAI_LLM_MAX_TRIES,
        max_time=config.OPENAI_LLM_MAX_TIME,
        base=config.OPENAI_LLM_BACKOFF_BASE,
        jitter=(
            backoff.full_jitter if config.OPENAI_LLM_BACKOFF_JITTER else None
        ),
    )
    @abstractmethod
    def invoke(
        self, system: str, human: str, images: list[str] | None = None
    ) -> str | dict:
        raise NotImplementedError(
            "invoke has not been defined for this class."
        )

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=config.OPENAI_LLM_MAX_TRIES,
        max_time=config.OPENAI_LLM_MAX_TIME,
        base=config.OPENAI_LLM_BACKOFF_BASE,
        jitter=(
            backoff.full_jitter if config.OPENAI_LLM_BACKOFF_JITTER else None
        ),
    )
    @abstractmethod
    async def ainvoke(
        self, system: str, human: str, images: list[str] | None = None
    ) -> str | dict:
        raise NotImplementedError(
            "ainvoke has not been defined for this class."
        )
