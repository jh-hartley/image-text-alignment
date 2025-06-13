from langchain_openai import OpenAIEmbeddings

from src.common.new_llm.base_embedding import BaseEmbeddingProvider
from src.common.new_llm.registry import register_embedding_provider
from src.config import config


@register_embedding_provider("openai")
class OpenAiEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, model: str | None = None):
        self._client = OpenAIEmbeddings(
            model=model or config.OPENAI_EMBEDDING_MODEL
        )

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        return await self._client.aembed_documents(texts)
