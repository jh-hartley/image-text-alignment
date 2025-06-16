from typing import Type, TypeVar

from pydantic import BaseModel

from src.common.llm.models import EmbeddingClient, LlmClient

T = TypeVar("T", bound=BaseModel)


class BaseLlmClient(LlmClient):
    """Base class for LLM provider implementations."""

    def invoke(
        self,
        system: str,
        human: str,
        output_type: Type[T] | None = None,
    ) -> T | str:
        raise NotImplementedError()

    async def ainvoke(
        self,
        system: str,
        human: str,
        output_type: Type[T] | None = None,
    ) -> T | str:
        raise NotImplementedError()


class BaseEmbeddingClient(EmbeddingClient):
    """Base class for embedding provider implementations."""

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError()
