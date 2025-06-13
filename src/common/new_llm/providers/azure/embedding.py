from langchain_openai import AzureOpenAIEmbeddings
from pydantic import SecretStr

from src.common.new_llm.base_embedding import BaseEmbeddingProvider
from src.common.new_llm.registry import register_embedding_provider
from src.config import config


@register_embedding_provider("azure")
class AzureEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, model: str | None = None):
        self._client = AzureOpenAIEmbeddings(
            api_key=SecretStr(config.AZURE_OPENAI_API_KEY),
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_version=config.AZURE_OPENAI_EMBEDDING_API_VERSION,
            azure_deployment=model or config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        )

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        return await self._client.aembed_documents(texts)
