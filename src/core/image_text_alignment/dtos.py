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
