from src.common.llm import ImageEncoder, Llm
from src.core.image_text_alignment.dtos import (
    ProductImageCheckInput,
    ProductImageCheckLLMResponse,
    ProductImageCheckResult,
)

from .prompts import PRODUCT_IMAGE_SYSTEM_PROMPT


class ProductImageLLMChecker:
    def __init__(self, llm: Llm, image_encoder: ImageEncoder | None = None):
        self.llm = llm
        self.image_encoder = image_encoder or ImageEncoder()
        self.system_prompt = PRODUCT_IMAGE_SYSTEM_PROMPT

    async def check(
        self, input: ProductImageCheckInput
    ) -> ProductImageCheckResult:
        human_prompt = input.description
        image = input.image

        prediction: ProductImageCheckLLMResponse = await self.llm.ainvoke(
            system=self.system_prompt,
            human=human_prompt,
            output_type=ProductImageCheckLLMResponse,
            images=[image],
        )
        return ProductImageCheckResult(
            product_key=input.product_key,
            is_mismatch=prediction.is_mismatch,
            justification=prediction.justification,
            description_synthesis=prediction.description_synthesis,
            image_summary=prediction.image_summary,
        )
