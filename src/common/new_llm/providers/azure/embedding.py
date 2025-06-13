import logging

from langchain_openai import AzureOpenAIEmbeddings
from pydantic import SecretStr

from src.common.logs import setup_logging
from src.common.new_llm.base_classes import BaseEmbeddingProvider
from src.common.new_llm.registry import register_provider
from src.config import config

from .constants import PROVIDER

logger = logging.getLogger(__name__)
setup_logging()


@register_provider("embedding", PROVIDER)
class AzureEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self):
        self._client = AzureOpenAIEmbeddings(
            api_key=SecretStr(config.AZURE_OPENAI_API_KEY),
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_version=config.AZURE_OPENAI_API_VERSION,
            azure_deployment=config.AZURE_OPENAI_DEPLOYMENT,
        )

    def get_embedding(self, text: str) -> list[float]:
        return self._client.embed_query(text)

    async def aget_embedding(self, text: str) -> list[float]:
        return await self._client.aembed_query(text)

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        return self._client.embed_documents(texts)

    async def aget_embeddings(self, texts: list[str]) -> list[list[float]]:
        return await self._client.aembed_documents(texts)
