from src.common.llm import ImageEncoder, Llm
from src.core.image_text_alignment.dtos import (
    ProductImageCheckInput,
    ProductImageCheckLLMResponse,
    ProductImageClassificationResult,
)

from .prompts import CLASSIFIER_PROMPT


class ProductImageLLMClassifier:
    def __init__(self, llm: Llm, image_encoder: ImageEncoder | None = None):
        self.llm = llm
        self.image_encoder = image_encoder or ImageEncoder()
        self.system_prompt: str = CLASSIFIER_PROMPT

    async def classify_image_colour(
        self, input: ProductImageCheckInput
    ) -> ProductImageClassificationResult:
        human_prompt = input.description
        image = input.image

        prediction: ProductImageCheckLLMResponse = await self.llm.ainvoke(
            system=self.system_prompt,
            human=human_prompt,
            output_type=ProductImageCheckLLMResponse,
            images=[image],
        )
        return ProductImageClassificationResult(
            product_key=input.product_key,
            image_path=input.image,
            colour_status=prediction.colour_status,
            colour_justification=prediction.colour_justification,
            description_synthesis=prediction.description_synthesis,
            image_summary=prediction.image_summary,
        )
