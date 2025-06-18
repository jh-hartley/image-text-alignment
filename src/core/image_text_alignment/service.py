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
    ProductImageCheckResult,
)
from src.core.image_text_alignment.llm_checker import ProductImageLLMChecker
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
        self.llm_checker = ProductImageLLMChecker(llm)
        self.logger = logger or logging.getLogger(__name__)
        self.image_encoder = ImageEncoder()
        self.max_workers = max_workers or config.DB_ASYNC_POOL_SIZE

    async def check_images_for_products(
        self, product_keys: list[str], batch_key: UUID | None = None
    ) -> list[ProductImageCheckResult]:
        """
        Process specific product keys, optionally as part of a batch.
        If no batch_key is provided, generates a new one.
        Allows overwriting existing predictions, updating their timestamps.
        """
        if batch_key is None:
            batch_key = uuid()

        # Process in chunks based on max_workers
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
    ) -> ProductImageCheckResult:
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
            result = ProductImageCheckResult(
                product_key=product_key,
                is_mismatch=False,
                justification="No product overview found.",
                image_path=None,
                description_synthesis="N/A",
                image_summary="N/A",
            )
            await self._store_result(batch_key, result)
            return result

        image_paths = [
            v for v in product.image_local_paths.model_dump().values() if v
        ]

        if not image_paths:
            self.logger.warning(
                f"No images found for product_key={product_key}"
            )
            result = ProductImageCheckResult(
                product_key=product_key,
                is_mismatch=False,
                justification="No images found.",
                image_path=None,
                description_synthesis="N/A",
                image_summary="N/A",
            )
            await self._store_result(batch_key, result)
            return result

        image_url = image_paths[0]
        image_result = load_image_bytes_from_url(image_url)
        if image_result.image_bytes is None:
            self.logger.warning(f"Image file not found: {image_url}")
            result = ProductImageCheckResult(
                product_key=product_key,
                is_mismatch=False,
                justification="Image file not found.",
                image_path=image_result.filename,
                description_synthesis="N/A",
                image_summary="N/A",
            )
            await self._store_result(batch_key, result)
            return result

        image_str = self.image_encoder.encode_image(image_result.image_bytes)
        description = product.to_llm_string()
        input_dto = ProductImageCheckInput(
            product_key=product_key,
            description=description,
            image=image_str,
        )
        result = await self.llm_checker.check(input_dto)
        result.image_path = image_result.filename
        await self._store_result(batch_key, result)
        return result

    async def _store_result(
        self, batch_key: UUID, result: ProductImageCheckResult
    ) -> None:
        """
        Store or update a prediction result in the database.
        Updates the timestamps appropriately.
        """
        now = clock.now()
        record = ImagePredictionRecord(
            batch_key=batch_key,
            product_key=UUID(result.product_key),
            image_path=result.image_path,
            is_mismatch=result.is_mismatch,
            justification=result.justification,
            description_synthesis=result.description_synthesis,
            image_summary=result.image_summary,
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
