from abc import ABC, abstractmethod

from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    text: str | None = None
    image: bytes | None = None

    def __post_init_post_parse__(self) -> None:
        if (self.text is None and self.image is None) or (
            self.text is not None and self.image is not None
        ):
            raise ValueError(
                "Exactly one of 'text' or 'image' must be provided."
            )


class EmbeddingResponse(BaseModel):
    embedding: list[float]


class BaseEmbeddingProvider(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def embed_image(self, image: bytes) -> list[float]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def embed_multimodal(self, text: str, image: bytes) -> list[float]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def aembed_text(self, text: str) -> list[float]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def aembed_image(self, image: bytes) -> list[float]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def aembed_multimodal(self, text: str, image: bytes) -> list[float]:
        raise NotImplementedError("Subclasses must implement this method")
