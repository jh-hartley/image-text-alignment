from pydantic import BaseModel


class ProductImageCheckInput(BaseModel):
    product_key: str
    description: str
    image: str


class ProductImageCheckPrediction(BaseModel):
    is_mismatch: bool
    justification: str


class ProductImageCheckResult(BaseModel):
    product_key: str
    is_mismatch: bool
    justification: str
    image_path: str | None = None


class ImageLoadResult(BaseModel):
    image_bytes: bytes | None = None
    filename: str | None = None

    @classmethod
    def from_loader(
        cls, image_bytes: bytes | None, filename: str | None
    ) -> "ImageLoadResult":
        return cls(image_bytes=image_bytes, filename=filename)
