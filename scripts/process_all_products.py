import asyncio
import logging
import sys
from uuid import UUID

from sqlalchemy.orm import Session

from src.common.db.base import uuid as uuid4
from src.common.db.engine import engine
from src.common.llm import Llm
from src.core.image_text_alignment.repositories import (
    ProductOverviewRepository,
)
from src.core.image_text_alignment.service import ImageTextAlignmentService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(batch_key: str | None = None):
    async def run():
        with Session(engine) as session:
            if batch_key is not None:
                batch_uuid = UUID(batch_key)
                logger.info(f"Using provided batch key: {batch_uuid}")
            else:
                batch_uuid = uuid4()
                logger.info(f"Generated new batch key: {batch_uuid}")

            product_overview_repo = ProductOverviewRepository(session)
            llm = Llm()
            service = ImageTextAlignmentService(
                product_overview_repo=product_overview_repo, llm=llm
            )
            logger.info(f"Async worker pool size: {service.max_workers}")
            product_keys = service.check_unprocessed_products(
                session, batch_uuid
            )
            if not product_keys:
                logger.info("No unprocessed product keys found for the batch.")
                return
            logger.info(
                f"Starting processing for {len(product_keys)} "
                "unprocessed products."
            )

            results = await service.check_images_for_products(
                product_keys, batch_key=batch_uuid
            )
            logger.info(
                f"Processing complete. {len(results)} products processed."
            )

    asyncio.run(run())


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python process_all_products.py [BATCH_KEY]")
        sys.exit(1)
    batch_key = sys.argv[1] if len(sys.argv) == 2 else None
    main(batch_key)
