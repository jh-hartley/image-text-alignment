import logging

from src.common.image_encoding import image_file_to_bytes
from src.common.llm import ImageEncoder, Llm
from src.core.image_text_alignment.dtos import (
    ProductImageCheckInput,
    ProductImageCheckResult,
)
from src.core.image_text_alignment.llm_checker import ProductImageLLMChecker
from src.core.image_text_alignment.records import ProductOverviewRecord
from src.core.image_text_alignment.repositories import (
    ProductOverviewRepository,
)


class ImageTextAlignmentService:
    def __init__(
        self,
        product_overview_repo: ProductOverviewRepository,
        llm: Llm,
        logger: logging.Logger | None = None,
    ) -> None:
        self.product_overview_repo = product_overview_repo
        self.llm_checker = ProductImageLLMChecker(llm)
        self.logger = logger or logging.getLogger(__name__)
        self.image_encoder = ImageEncoder()

    async def check_images_for_products(
        self, product_keys: list[str]
    ) -> list[ProductImageCheckResult]:
        results: list[ProductImageCheckResult] = []

        for product_key in product_keys:
            product = self.product_overview_repo.get_product_overview(
                product_key
            )

            if product is None:
                self._log_and_append_result(
                    results, product_key, "No product overview found."
                )
                continue

            image_paths = self._get_image_paths(product)

            if not image_paths:
                self._log_and_append_result(
                    results, product_key, "No images found."
                )
                continue

            image_path = image_paths[0]
            self.logger.info(
                f"Checking image for product_key={product_key}: {image_path}"
            )
            try:
                image_bytes = image_file_to_bytes(image_path)
            except FileNotFoundError:
                self._log_and_append_result(
                    results, product_key, "Image file not found."
                )
                continue

            description = product.to_llm_string()
            input_dto = ProductImageCheckInput(
                product_key=product_key,
                description=description,
                image=self.image_encoder.encode_image(image_bytes),
            )
            result = await self.llm_checker.check(input_dto)
            results.append(result)

        return results

    def _log_and_append_result(
        self,
        results: list[ProductImageCheckResult],
        product_key: str,
        justification: str,
    ) -> None:
        self.logger.warning(f"{justification} for product_key={product_key}")
        results.append(
            ProductImageCheckResult(
                product_key=product_key,
                is_mismatch=False,
                justification=justification,
            )
        )

    def _get_image_paths(self, product: ProductOverviewRecord) -> list[str]:
        return [
            v for v in product.image_local_paths.model_dump().values() if v
        ]

    def _encode_image(self, image_path: str) -> str:
        image_bytes = image_file_to_bytes(image_path)
        return self.image_encoder.encode_image(image_bytes)
