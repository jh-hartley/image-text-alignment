import logging
from typing import Type, TypeVar, cast

import backoff
from pydantic import BaseModel

from src.common.llm.registry import get_provider
from src.common.logging import setup_logging
from src.config import config

logger = logging.getLogger(__name__)
setup_logging()

T = TypeVar("T", bound=BaseModel)


class Llm:
    """Main class for handling LLM interactions."""

    def __init__(self) -> None:
        provider = config.LLM_PROVIDER.lower()
        logger.debug(f"Initialising LLM provider: {provider}")
        provider_cls = get_provider("llm", provider)
        self._provider = provider_cls()

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
    def invoke(
        self,
        system: str,
        human: str,
        output_type: Type[T] | None = None,
        images: list[str] | None = None,
    ) -> T | str:
        output = cast(str, self._provider.invoke(system, human, images))
        if output_type:
            return output_type.model_validate_json(output)
        return output

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
    async def ainvoke(
        self,
        system: str,
        human: str,
        output_type: Type[T] | None = None,
        images: list[str] | None = None,
    ) -> T | str:
        """Invoke the LLM asynchronously."""
        output = cast(str, await self._provider.ainvoke(system, human, images))
        if output_type:
            return output_type.model_validate_json(output)
        return output
