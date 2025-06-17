import base64
import logging

from langchain_openai import AzureOpenAIEmbeddings
from pydantic import SecretStr

from src.common.llm.base_classes.base_embedding import (
    BaseEmbeddingProvider,
)
from src.common.llm.registry import register_provider
from src.common.logs import setup_logging
from src.config import config

logger = logging.getLogger(__name__)
setup_logging()

PROVIDER = "azure"


@register_provider("embedding", PROVIDER)
class AzureEmbeddingProvider(BaseEmbeddingProvider):

    def __init__(self) -> None:
        self._client = AzureOpenAIEmbeddings(
            azure_deployment=config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
            api_version=config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=SecretStr(config.AZURE_OPENAI_API_KEY),
            model=config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        )

    def embed_text(self, text: str) -> list[float]:
        logger.debug(f"Embedding text: {text[:50]}...")
        return self._client.embed_query(text)

    def embed_image(self, image: bytes) -> list[float]:
        logger.debug("Embedding image")
        image_data = base64.b64encode(image).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{image_data}"
        return self._client.embed_query(data_url)

    def embed_multimodal(self, text: str, image: bytes) -> list[float]:
        logger.debug(
            f"Embedding multimodal for text: {text[:50]}... and image"
        )
        image_data = base64.b64encode(image).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{image_data}"
        prompt = f"{text}\n{data_url}"
        return self._client.embed_query(prompt)

    async def aembed_text(self, text: str) -> list[float]:
        logger.debug(f"Async embedding text: {text[:50]}...")
        return await self._client.aembed_query(text)

    async def aembed_image(self, image: bytes) -> list[float]:
        logger.debug("Async embedding image")
        image_data = base64.b64encode(image).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{image_data}"
        return await self._client.aembed_query(data_url)

    async def aembed_multimodal(self, text: str, image: bytes) -> list[float]:
        logger.debug(
            f"Async embedding multimodal for text: {text[:50]}... and image"
        )
        image_data = base64.b64encode(image).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{image_data}"
        prompt = f"{text}\n{data_url}"
        return await self._client.aembed_query(prompt)
