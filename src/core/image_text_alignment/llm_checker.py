from src.common.llm import ImageEncoder, Llm

from .dtos import (
    ProductImageCheckInput,
    ProductImageCheckPrediction,
    ProductImageCheckResult,
)
from .prompts import PRODUCT_IMAGE_SYSTEM_PROMPT


class ProductImageLLMChecker:
    def __init__(self, llm: Llm, image_encoder: ImageEncoder | None = None):
        self.llm = llm
        self.image_encoder = image_encoder or ImageEncoder()
        self.system_prompt = PRODUCT_IMAGE_SYSTEM_PROMPT
        if not self.system_prompt:
            raise ValueError(
                "System prompt for ProductImageLLMChecker could not be loaded."
            )

    async def check(
        self, input: ProductImageCheckInput
    ) -> ProductImageCheckResult:
        human_prompt = input.description
        image = input.image

        prediction: ProductImageCheckPrediction = await self.llm.ainvoke(
            system=self.system_prompt,
            human=human_prompt,
            output_type=ProductImageCheckPrediction,
            images=[image],
        )
        return ProductImageCheckResult(
            product_key=input.product_key,
            is_mismatch=prediction.is_mismatch,
            justification=prediction.justification,
        )
