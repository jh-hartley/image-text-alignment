from typing import cast

from src.common.new_llm.registry import EMBEDDING_PROVIDERS
from src.config import config


class Embedding:
    def __init__(self) -> None:
        provider_name = config.LLM_PROVIDER
        provider_cls = EMBEDDING_PROVIDERS.get(provider_name)
        if provider_cls is None:
            raise ValueError(f"Unknown Embedding provider: {provider_name}")
        self._provider = provider_cls()

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        result = await self._provider.aembed_documents(texts)
        return cast(list[list[float]], result)
