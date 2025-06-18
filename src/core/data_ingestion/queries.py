from sqlalchemy import func
from src.core.data_ingestion.records import (
    ProductRecord,
    ProductCategoryRecord,
    CategoryRecord,
    ProductAttributeValueRecord,
    AttributeRecord,
)
from sqlalchemy.orm import Session
from typing import Sequence


def get_random_product_keys(
    session: Session, n: int, category_name: str | None = None
) -> Sequence[str]:
    query = session.query(ProductRecord.product_key)
    if category_name:
        category_keys = [
            row.category_key
            for row in session.query(CategoryRecord.category_key)
            .filter(CategoryRecord.friendly_name == category_name)
            .all()
        ]
        if not category_keys:
            return []
        query = (
            query.join(
                ProductCategoryRecord,
                ProductRecord.product_key == ProductCategoryRecord.product_key,
            )
            .filter(ProductCategoryRecord.category_key.in_(category_keys))
        )
    query = query.order_by(func.random()).limit(n)
    return [str(row[0]) for row in query.all()]


def get_random_product_keys_by_colour(
    session: Session, n: int, colour_value: str
) -> Sequence[str]:
    colour_attr = (
        session.query(AttributeRecord)
        .filter(AttributeRecord.friendly_name == "colour")
        .first()
    )
    if not colour_attr:
        return []
    colour_key = colour_attr.attribute_key

    query = (
        session.query(ProductAttributeValueRecord.product_key)
        .filter(
            ProductAttributeValueRecord.attribute_key == colour_key,
            ProductAttributeValueRecord.value == colour_value,
        )
        .order_by(func.random())
        .limit(n)
    )
    return [str(row[0]) for row in query.all()]