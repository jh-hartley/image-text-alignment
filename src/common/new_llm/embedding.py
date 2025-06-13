import logging
from itertools import islice
from typing import Iterable, Iterator, cast

import numpy as np
import tiktoken

from src.common.logs import setup_logging
from src.common.new_llm.registry import get_provider
from src.config import config

logger = logging.getLogger(__name__)
setup_logging()


class Embedding:
    """Main class for handling embeddings."""

    def __init__(self) -> None:
        """Initialize the embedding provider based on configuration."""
        provider = config.LLM_PROVIDER.lower()
        logger.debug(f"Initializing embedding provider: {provider}")
        provider_cls = get_provider("embedding", provider)
        self._provider = provider_cls()

    def _get_encoding_name(self) -> str:
        """Get the encoding name for the current provider's model."""
        if config.LLM_PROVIDER == "azure":
            model_name = config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT
        else:
            model_name = config.OPENAI_EMBEDDING_MODEL

        if model_name in {
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "text-embedding-3-large",
        }:
            return "cl100k_base"
        if model_name in {
            "ada-002",
            "text-embedding-3-small",
            "text-embedding-3-large",
        }:
            return "cl100k_base"
        raise ValueError(f"Unknown embedding model: {model_name}")

    def _batched(self, iterable: Iterable, n: int) -> Iterator[tuple]:
        """Split an iterable into batches of size n."""
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(islice(it, n)):
            yield batch

    def _chunked_tokens(
        self, text: str, chunk_length: int
    ) -> Iterator[tuple[int]]:
        """Split text into chunks of tokens."""
        encoding_name = self._get_encoding_name()
        encoding = tiktoken.get_encoding(encoding_name)
        tokens = encoding.encode(text)
        yield from self._batched(tokens, chunk_length)

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        result = await self._provider.aembed_documents(texts)
        return cast(list[list[float]], result)

    async def len_safe_get_embedding(
        self, text: str, chunk_size: int | None = None
    ) -> tuple[list[list[float]], list[int]]:
        """Get embeddings for text that may exceed token limits by chunking."""
        chunk_embeddings = []
        chunk_lengths = []

        chunk_size = chunk_size or config.EMBEDDING_DEFAULT_DIMENSIONS
        encoding_name = self._get_encoding_name()
        encoding = tiktoken.get_encoding(encoding_name)

        for chunk in self._chunked_tokens(text, chunk_size):
            chunk_text = encoding.decode(chunk)
            embedding = (await self.aembed_documents([chunk_text]))[0]
            chunk_embeddings.append(embedding)
            chunk_lengths.append(len(chunk))

        return chunk_embeddings, chunk_lengths

    async def len_safe_get_averaged_embedding(
        self, text: str, chunk_size: int | None = None
    ) -> list[float]:
        """Get a length-safe averaged embedding for the input text."""
        chunk_embeddings, chunk_lengths = await self.len_safe_get_embedding(
            text, chunk_size
        )
        averaged_embedding = np.average(
            chunk_embeddings, axis=0, weights=chunk_lengths
        )
        normalised_embedding = averaged_embedding / np.linalg.norm(
            averaged_embedding
        )
        return normalised_embedding.tolist()

    def get_embedding(self, text: str) -> list[float]:
        """Get embedding for a single text string."""
        logger.debug(f"Getting embedding for text: {text[:50]}...")
        return self._provider.get_embedding(text)

    async def aget_embedding(self, text: str) -> list[float]:
        """Get embedding for a single text string asynchronously."""
        logger.debug(
            f"Getting embedding asynchronously for text: {text[:50]}..."
        )
        return await self._provider.aget_embedding(text)

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for a list of text strings."""
        logger.debug(f"Getting embeddings for {len(texts)} texts")
        return self._provider.get_embeddings(texts)

    async def aget_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for a list of text strings asynchronously."""
        logger.debug(
            f"Getting embeddings asynchronously for {len(texts)} texts"
        )
        return await self._provider.aget_embeddings(texts)
