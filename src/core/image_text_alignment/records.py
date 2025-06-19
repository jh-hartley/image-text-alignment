from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.common.db.base import Base
from src.core.image_text_alignment.dtos import ImagePredictionDTO


class Categories(BaseModel):
    category_0: str | None
    category_1: str | None
    category_2: str | None
    category_3: str | None


class Prices(BaseModel):
    now_price: str | None
    was_price: str | None
    save_message: str | None


class ImageLocalPaths(BaseModel):
    image_local_path_1: str | None
    image_local_path_2: str | None
    image_local_path_3: str | None
    image_local_path_4: str | None
    image_local_path_5: str | None
    image_local_path_6: str | None
    image_local_path_7: str | None
    image_local_path_8: str | None
    image_local_path_9: str | None
    image_local_path_10: str | None


class ProductOverviewRecord(BaseModel):
    """
    Synthetic record combining all product information used for LLM calls.

    None values are used to show that no value is in the DB.
    """

    product_key: UUID
    system_name: str | None
    friendly_name: str | None
    product_code: str | None
    product_title: str | None
    product_url: str | None
    categories: Categories
    description_text: str | None
    specification_text: str | None
    specification_attributes_xml: str | None
    image_local_paths: ImageLocalPaths
    prices: Prices
    on_promotion: str | None
    review_count: str | None
    review_rating: str | None
    attribute_values: list[dict[str, str | None]]

    def to_llm_string(self) -> str:
        lines = []
        lines.append(f"Product Title: {self.product_title}")
        lines.append(f"Product Code (EAN): {self.product_code}")
        if self.categories:
            cat_str = ", ".join(
                v for v in self.categories.model_dump().values() if v
            )
            lines.append(f"Categories: {cat_str}")
        if self.specification_text:
            lines.append(f"Specification: {self.specification_text}")
        if self.description_text:
            lines.append(f"Description: {self.description_text}")
        if self.attribute_values:
            lines.append("Attributes:")
            for attr in self.attribute_values:
                name = attr.get("attribute_name")
                value = attr.get("value")
                if name and value:
                    extras = []
                    for k in [
                        "unit",
                        "minimum_value",
                        "minimum_unit",
                        "maximum_value",
                        "maximum_unit",
                        "range_qualifier_enum",
                    ]:
                        v = attr.get(k)
                        if v is not None:
                            extras.append(f"{k}: {v}")
                    if extras:
                        lines.append(
                            f"  - {name}: {value} ({', '.join(extras)})"
                        )
                    else:
                        lines.append(f"  - {name}: {value}")
        return "\n".join(lines)


class ImagePredictionRecord(Base):
    __tablename__ = "image_prediction"
    batch_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    product_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    image_name = Column(Text)
    colour_status = Column(Text)
    colour_justification = Column(Text)
    image_summary = Column(Text)
    description_synthesis = Column(Text)
    final_colour_status = Column(Text)
    final_colour_justification = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in ImagePredictionDTO.model_fields
        }

    def to_model(self) -> ImagePredictionDTO:
        return ImagePredictionDTO(**self.to_dict())

    def to_dto(self) -> ImagePredictionDTO:
        return self.to_model()
