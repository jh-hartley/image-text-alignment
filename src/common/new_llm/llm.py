from typing import Type, TypeVar, cast

from pydantic import BaseModel

from src.common.new_llm.registry import LLM_PROVIDERS
from src.config import config

T = TypeVar("T", bound=BaseModel)


class Llm:
    def __init__(self) -> None:
        provider_name = config.LLM_PROVIDER
        provider_cls = LLM_PROVIDERS.get(provider_name)
        if provider_cls is None:
            raise ValueError(f"Unknown LLM provider: {provider_name}")
        self._provider = provider_cls()

    def invoke(
        self, system: str, human: str, output_type: Type[T] | None = None
    ) -> T | str:
        output = cast(str, self._provider.invoke(system, human))
        if output_type:
            return output_type.model_validate_json(output)
        return output

    async def ainvoke(
        self, system: str, human: str, output_type: Type[T] | None = None
    ) -> T | str:
        output = cast(str, self._provider.invoke(system, human))
        if output_type:
            return output_type.model_validate_json(output)
        return output
