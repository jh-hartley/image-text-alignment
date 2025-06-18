from pydantic import BaseModel


class ImageLoadResult(BaseModel):
    image_bytes: bytes | None
    filename: str | None

    @classmethod
    def from_loader(
        cls, image_bytes: bytes | None, filename: str | None
    ) -> "ImageLoadResult":
        return cls(image_bytes=image_bytes, filename=filename)
