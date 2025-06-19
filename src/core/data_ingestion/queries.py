import logging
from typing import Sequence

from sqlalchemy.orm import Session

from src.common.logging import setup_logging
from src.common.rng import get_rng
from src.core.data_ingestion.records import (
    AttributeRecord,
    CategoryRecord,
    DunelmCoalesceOutputRecord,
    ProductAttributeValueRecord,
    ProductCategoryRecord,
    ProductRecord,
)

logger = logging.getLogger(__name__)
setup_logging()


def get_random_product_keys(
    session: Session,
    n: int,
    category_name: str | None = None,
    seed: int | None = None,
) -> Sequence[str]:
    if seed is not None:
        logger.debug(f"Random seed for get_random_product_keys: {seed}")
    rng = get_rng(seed)

    query = session.query(ProductRecord.product_key)
    if category_name:
        category_keys = [
            row[0]
            for row in session.query(CategoryRecord.category_key).filter(
                CategoryRecord.friendly_name == category_name
            )
        ]
        if not category_keys:
            return []
        query = query.join(
            ProductCategoryRecord,
            ProductRecord.product_key == ProductCategoryRecord.product_key,
        ).filter(ProductCategoryRecord.category_key.in_(category_keys))

    valid_keys = [
        str(row[0])
        for row in query.join(
            DunelmCoalesceOutputRecord,
            ProductRecord.system_name
            == DunelmCoalesceOutputRecord.product_url,
        ).all()
    ]
    if not valid_keys:
        return []
    return rng.sample(valid_keys, min(n, len(valid_keys)))


def get_random_product_keys_by_colour(
    session: Session, n: int, colour_value: str, seed: int | None = None
) -> Sequence[str]:
    if seed is not None:
        logger.debug(
            f"Random seed for get_random_product_keys_by_colour: {seed}"
        )
    rng = get_rng(seed)

    colour_attr = (
        session.query(AttributeRecord)
        .filter(AttributeRecord.friendly_name == "colour")
        .first()
    )
    if not colour_attr:
        return []
    colour_key = colour_attr.attribute_key
    query = session.query(ProductAttributeValueRecord.product_key).filter(
        ProductAttributeValueRecord.attribute_key == colour_key,
        ProductAttributeValueRecord.value == colour_value,
    )

    valid_keys = [
        str(row[0])
        for row in query.join(
            ProductRecord,
            ProductAttributeValueRecord.product_key
            == ProductRecord.product_key,
        )
        .join(
            DunelmCoalesceOutputRecord,
            ProductRecord.system_name
            == DunelmCoalesceOutputRecord.product_url,
        )
        .all()
    ]
    if not valid_keys:
        return []
    return rng.sample(valid_keys, min(n, len(valid_keys)))
