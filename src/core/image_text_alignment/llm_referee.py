from src.common.llm import ImageEncoder, Llm
from src.core.image_text_alignment.dtos import (
    ProductImageRefereeInput,
    ProductImageRefereeLLMResponse,
    ProductImageRefereeResult,
)

from .prompts import REFEREE_PROMPT


class ProductImageLLMReferee:
    def __init__(self, llm: Llm, image_encoder: ImageEncoder | None = None):
        self.llm = llm
        self.image_encoder = image_encoder or ImageEncoder()
        self.system_prompt: str = REFEREE_PROMPT

    async def referee(
        self, input: ProductImageRefereeInput
    ) -> ProductImageRefereeResult:
        human_prompt = f"""Product Description: {input.description}

Classifier Output:
- colour_status: {input.classifier_colour_status}
- colour_justification: {input.classifier_colour_justification}
- image_summary: {input.classifier_image_summary}
- description_synthesis: {input.classifier_description_synthesis}"""

        image = input.image

        prediction: ProductImageRefereeLLMResponse = await self.llm.ainvoke(
            system=self.system_prompt,
            human=human_prompt,
            output_type=ProductImageRefereeLLMResponse,
            images=[image],
        )
        return ProductImageRefereeResult(
            final_colour_status=prediction.final_colour_status,
            final_colour_justification=prediction.final_colour_justification,
        )
