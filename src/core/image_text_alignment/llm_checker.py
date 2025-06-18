from src.common.llm import ImageEncoder, Llm

from .dtos import (
    ProductImageCheckInput,
    ProductImageCheckPrediction,
    ProductImageCheckResult,
)


class ProductImageLLMChecker:
    def __init__(self, llm: Llm, image_encoder: ImageEncoder | None = None):
        self.llm = llm
        self.image_encoder = image_encoder or ImageEncoder()

    async def check(
        self, input: ProductImageCheckInput
    ) -> ProductImageCheckResult:
        system_prompt = (
            "You are an expert in product compliance. Your job is to identify "
            "cases where a product image could not possibly correspond to the "
            "product as described, in order to avoid regulatory fines. Only "
            "respond 'True' if you are certain the image does NOT match the "
            "description. Also provide a short justification.\n"
            "Return only a valid JSON object with the following structure "
            "and nothing else (no markdown, no code block, no extra text):\n"
            '{"is_mismatch": <true_or_false>, "justification": <string>}'
        )
        human_prompt = input.description
        image = input.image

        prediction: ProductImageCheckPrediction = await self.llm.ainvoke(
            system=system_prompt,
            human=human_prompt,
            output_type=ProductImageCheckPrediction,
            images=[image],
        )
        return ProductImageCheckResult(
            product_key=input.product_key,
            is_mismatch=prediction.is_mismatch,
            justification=prediction.justification,
        )
