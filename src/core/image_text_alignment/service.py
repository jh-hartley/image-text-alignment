import asyncio
import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.common.clock import clock
from src.common.db.async_session import async_engine
from src.common.db.base import uuid
from src.common.llm import ImageEncoder, Llm
from src.config import config
from src.core.data_ingestion.repositories import ProductRepository
from src.core.image_encoding import load_image_bytes_from_url
from src.core.image_text_alignment.dtos import (
    ProductImageCheckInput,
    ProductImageClassificationResult,
    ProductImageRefereeInput,
    ProductImageRefereeResult,
)
from src.core.image_text_alignment.llm_classifier import (
    ProductImageLLMClassifier,
)
from src.core.image_text_alignment.llm_referee import ProductImageLLMReferee
from src.core.image_text_alignment.records import (
    ImagePredictionRecord,
    ProductOverviewRecord,
)
from src.core.image_text_alignment.repositories import (
    AsyncImagePredictionRepository,
    ImagePredictionRepository,
    ProductOverviewRepository,
)


class ImageTextAlignmentService:
    def __init__(
        self,
        product_overview_repo: ProductOverviewRepository,
        llm: Llm,
        logger: logging.Logger | None = None,
        max_workers: int | None = None,
    ) -> None:
        self.product_overview_repo = product_overview_repo
        self.llm_checker = ProductImageLLMClassifier(llm)
        self.llm_referee = ProductImageLLMReferee(llm)
        self.logger = logger or logging.getLogger(__name__)
        self.image_encoder = ImageEncoder()
        self.max_workers = max_workers or config.DB_ASYNC_POOL_SIZE

    async def check_images_for_products(
        self, product_keys: list[str], batch_key: UUID | None = None
    ) -> list[ProductImageClassificationResult]:
        """
        Process specific product keys, optionally as part of a batch.
        If no batch_key is provided, generates a new one.
        Allows overwriting existing predictions, updating their timestamps.
        """
        if batch_key is None:
            batch_key = uuid()

        chunks = [
            product_keys[i : i + self.max_workers]
            for i in range(0, len(product_keys), self.max_workers)
        ]

        all_results = []
        for chunk in chunks:
            tasks = [
                self._process_single_product(batch_key, product_key)
                for product_key in chunk
            ]
            chunk_results = await asyncio.gather(*tasks)
            all_results.extend(chunk_results)

        return all_results

    def check_unprocessed_products(
        self, session: Session, batch_key: UUID
    ) -> list[str]:
        product_repo = ProductRepository(session)
        prediction_repo = ImagePredictionRepository(session)
        all_products = product_repo.find()
        processed = set(
            r.product_key
            for r in prediction_repo.find_by_batch(str(batch_key))
        )
        unprocessed = [
            str(p.product_key)
            for p in all_products
            if p.product_key not in processed
        ]
        return unprocessed

    async def _process_single_product(
        self, batch_key: UUID, product_key: str
    ) -> ProductImageClassificationResult:
        """
        Process a single product and store its result.
        This is an atomic operation that includes both processing and storage.
        """
        product: ProductOverviewRecord | None = (
            self.product_overview_repo.get_product_overview(product_key)
        )

        if not product:
            self.logger.warning(
                f"No product overview found for product_key={product_key}"
            )
            result = ProductImageClassificationResult(
                product_key=product_key,
                colour_status="N/A",
                colour_justification="No product overview found.",
                image_path=None,
                description_synthesis="N/A",
                image_summary="N/A",
            )
            referee_result = ProductImageRefereeResult(
                final_colour_status="N/A",
                final_colour_justification="No product overview found.",
            )
            await self._store_result(batch_key, result, referee_result)
            return result

        image_paths = [
            v for v in product.image_local_paths.model_dump().values() if v
        ]

        if not image_paths:
            self.logger.warning(
                f"No images found for product_key={product_key}"
            )
            result = ProductImageClassificationResult(
                product_key=product_key,
                colour_status="N/A",
                colour_justification="No images found.",
                image_path=None,
                description_synthesis="N/A",
                image_summary="N/A",
            )
            referee_result = ProductImageRefereeResult(
                final_colour_status="N/A",
                final_colour_justification="No images found.",
            )
            await self._store_result(batch_key, result, referee_result)
            return result

        image_url = image_paths[0]
        image_result = load_image_bytes_from_url(image_url)
        if image_result.image_bytes is None:
            self.logger.warning(f"Image file not found: {image_url}")
            result = ProductImageClassificationResult(
                product_key=product_key,
                colour_status="N/A",
                colour_justification="Image file not found.",
                image_path=image_result.filename,
                description_synthesis="N/A",
                image_summary="N/A",
            )
            referee_result = ProductImageRefereeResult(
                final_colour_status="N/A",
                final_colour_justification="Image file not found.",
            )
            await self._store_result(batch_key, result, referee_result)
            return result

        image_str = self.image_encoder.encode_image(image_result.image_bytes)
        description = product.to_llm_string()
        input_dto = ProductImageCheckInput(
            product_key=product_key,
            description=description,
            image=image_str,
        )
        result = await self.llm_checker.classify_image_colour(input_dto)
        result.image_path = image_result.filename

        # Only call referee if the classifier result is not "MATCH"
        if result.colour_status != "MATCH":
            referee_input = ProductImageRefereeInput(
                product_key=product_key,
                description=description,
                image=image_str,
                classifier_colour_status=result.colour_status,
                classifier_colour_justification=result.colour_justification,
                classifier_image_summary=result.image_summary,
                classifier_description_synthesis=result.description_synthesis,
            )
            referee_result = await self.llm_referee.referee(referee_input)
        else:
            # If it's a match, use the classifier's result as the final result
            referee_result = ProductImageRefereeResult(
                final_colour_status=result.colour_status,
                final_colour_justification=result.colour_justification,
            )

        await self._store_result(batch_key, result, referee_result)
        return result

    async def _store_result(
        self,
        batch_key: UUID,
        result: ProductImageClassificationResult,
        referee_result: ProductImageRefereeResult,
    ) -> None:
        """
        Store or update a prediction result in the database.
        Updates the timestamps appropriately.
        """
        now = clock.now()
        image_path = result.image_path
        if image_path and image_path.startswith("data/image/"):
            image_path = image_path[len("data/image/") :]
        record = ImagePredictionRecord(
            batch_key=batch_key,
            product_key=UUID(result.product_key),
            image_name=image_path,
            colour_status=result.colour_status,
            colour_justification=result.colour_justification,
            description_synthesis=result.description_synthesis,
            image_summary=result.image_summary,
            final_colour_status=referee_result.final_colour_status,
            final_colour_justification=referee_result.final_colour_justification,
            created_at=now,
            updated_at=now,
        )
        async with AsyncSession(async_engine) as async_session:
            image_prediction_repo = AsyncImagePredictionRepository(
                async_session
            )
            await image_prediction_repo.add(record)

    def _get_image_paths(self, product: ProductOverviewRecord) -> list[str]:
        return [
            v for v in product.image_local_paths.model_dump().values() if v
        ]
