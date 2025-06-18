from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.common.db.base import Base

from .dtos import (
    AttributeAllowableValueInAnyCategoryDTO,
    AttributeAllowableValuesApplicableInEveryCategoryDTO,
    AttributeDTO,
    CategoryAllowableValueDTO,
    CategoryAttributeDTO,
    CategoryDTO,
    DunelmCoalesceOutputDTO,
    ImageFilePathMappingDTO,
    ProductAttributeAllowableValueDTO,
    ProductAttributeGapsDTO,
    ProductAttributeValueDTO,
    ProductCategoryDTO,
    ProductDTO,
    RecommendationDTO,
    RecommendationRoundDTO,
    RichTextSourceDTO,
)


class DunelmCoalesceOutputRecord(Base):
    __tablename__ = "dunelm_coalesce_output"
    product_code = Column(String, primary_key=True)
    product_title = Column(String)
    product_url = Column(String)
    category_0 = Column(String)
    category_1 = Column(String)
    category_2 = Column(String)
    category_3 = Column(String)
    category_1_n = Column(String)
    category_1_n_url = Column(String)
    category_2_n = Column(String)
    category_2_n_url = Column(String)
    category_3_n = Column(String)
    category_3_n_url = Column(String)
    category_0_p = Column(String)
    category_1_p = Column(String)
    category_2_p = Column(String)
    category_3_p = Column(String)
    description_text = Column(String)
    specification_text = Column(String)
    specification_attributes_xml = Column(String)
    image_url_1 = Column(String)
    image_url_2 = Column(String)
    image_url_3 = Column(String)
    image_url_4 = Column(String)
    image_url_5 = Column(String)
    image_url_6 = Column(String)
    image_url_7 = Column(String)
    image_url_8 = Column(String)
    image_url_9 = Column(String)
    image_url_10 = Column(String)
    description_bullet_points = Column(String)
    now_price = Column(String)
    was_price = Column(String)
    save_message = Column(String)
    on_promotion = Column(String)
    video = Column(String)
    review_count = Column(String)
    review_rating = Column(String)
    image_g = Column(String)
    roundel_g = Column(String)
    conscious_choice = Column(String)
    returns = Column(String)
    dunelm_dimensions_attributes_xml = Column(String)
    sample = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in DunelmCoalesceOutputDTO.model_fields
        }

    def to_model(self) -> DunelmCoalesceOutputDTO:
        return DunelmCoalesceOutputDTO(**self.to_dict())

    def to_dto(self) -> DunelmCoalesceOutputDTO:
        return self.to_model()


class ImageFilePathMappingRecord(Base):
    __tablename__ = "image_file_path_mapping"
    image_path = Column(String, primary_key=True)
    image_url = Column(String)
    product_url = Column(String)
    position = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in ImageFilePathMappingDTO.model_fields
        }

    def to_model(self) -> ImageFilePathMappingDTO:
        return ImageFilePathMappingDTO(**self.to_dict())

    def to_dto(self) -> ImageFilePathMappingDTO:
        return self.to_model()


class RichTextSourceRecord(Base):
    __tablename__ = "rich_text_source"
    product_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    rich_text = Column(String)
    rich_text_name = Column(String)
    rich_text_priority = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in RichTextSourceDTO.model_fields
        }

    def to_model(self) -> RichTextSourceDTO:
        return RichTextSourceDTO(**self.to_dict())

    def to_dto(self) -> RichTextSourceDTO:
        return self.to_model()


class RecommendationRoundRecord(Base):
    __tablename__ = "recommendation_round"
    recommendation_round_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    round_name = Column(String)
    timestamp = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in RecommendationRoundDTO.model_fields
        }

    def to_model(self) -> RecommendationRoundDTO:
        return RecommendationRoundDTO(**self.to_dict())

    def to_dto(self) -> RecommendationRoundDTO:
        return self.to_model()


class RecommendationRecord(Base):
    __tablename__ = "recommendation"
    product_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    recommended_value = Column(String)
    unit = Column(String)
    minimum_value = Column(String)
    minimum_unit = Column(String)
    maximum_value = Column(String)
    maximum_unit = Column(String)
    original_expression = Column(String)
    range_qualifier_enum = Column(String)
    confidence_score = Column(String)
    recommendation_round_key = Column(PG_UUID(as_uuid=True))
    is_disallowed = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in RecommendationDTO.model_fields
        }

    def to_model(self) -> RecommendationDTO:
        return RecommendationDTO(**self.to_dict())

    def to_dto(self) -> RecommendationDTO:
        return self.to_model()


class ProductCategoryRecord(Base):
    __tablename__ = "product_category"
    product_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    category_key = Column(PG_UUID(as_uuid=True), primary_key=True)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in ProductCategoryDTO.model_fields
        }

    def to_model(self) -> ProductCategoryDTO:
        return ProductCategoryDTO(**self.to_dict())

    def to_dto(self) -> ProductCategoryDTO:
        return self.to_model()


class ProductAttributeValueRecord(Base):
    __tablename__ = "product_attribute_value"
    product_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    value = Column(String)
    unit = Column(String)
    minimum_value = Column(String)
    minimum_unit = Column(String)
    maximum_value = Column(String)
    maximum_unit = Column(String)
    range_qualifier_enum = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in ProductAttributeValueDTO.model_fields
        }

    def to_model(self) -> ProductAttributeValueDTO:
        return ProductAttributeValueDTO(**self.to_dict())

    def to_dto(self) -> ProductAttributeValueDTO:
        return self.to_model()


class ProductAttributeGapsRecord(Base):
    __tablename__ = "product_attribute_gaps"
    product_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    is_non_fillable = Column(String)
    non_fillable_reason = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in ProductAttributeGapsDTO.model_fields
        }

    def to_model(self) -> ProductAttributeGapsDTO:
        return ProductAttributeGapsDTO(**self.to_dict())

    def to_dto(self) -> ProductAttributeGapsDTO:
        return self.to_model()


class ProductAttributeAllowableValueRecord(Base):
    __tablename__ = "product_attribute_allowable_value"
    product_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    value = Column(String)
    minimum_value = Column(String)
    minimum_unit = Column(String)
    maximum_value = Column(String)
    maximum_unit = Column(String)
    range_qualifier_enum = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in ProductAttributeAllowableValueDTO.model_fields
        }

    def to_model(self) -> ProductAttributeAllowableValueDTO:
        return ProductAttributeAllowableValueDTO(**self.to_dict())

    def to_dto(self) -> ProductAttributeAllowableValueDTO:
        return self.to_model()


class ProductRecord(Base):
    __tablename__ = "product"
    product_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    system_name = Column(String)
    friendly_name = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field) for field in ProductDTO.model_fields
        }

    def to_model(self) -> ProductDTO:
        return ProductDTO(**self.to_dict())

    def to_dto(self) -> ProductDTO:
        return self.to_model()


class CategoryAttributeRecord(Base):
    __tablename__ = "category_attribute"
    category_attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    category_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in CategoryAttributeDTO.model_fields
        }

    def to_model(self) -> CategoryAttributeDTO:
        return CategoryAttributeDTO(**self.to_dict())

    def to_dto(self) -> CategoryAttributeDTO:
        return self.to_model()


class CategoryAllowableValueRecord(Base):
    __tablename__ = "category_allowable_value"
    category_attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    allowable_value = Column(String)
    allowable_unit_type = Column(String)
    minimum_value = Column(String)
    minimum_unit = Column(String)
    maximum_value = Column(String)
    maximum_unit = Column(String)
    range_qualifier_enum = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in CategoryAllowableValueDTO.model_fields
        }

    def to_model(self) -> CategoryAllowableValueDTO:
        return CategoryAllowableValueDTO(**self.to_dict())

    def to_dto(self) -> CategoryAllowableValueDTO:
        return self.to_model()


class CategoryRecord(Base):
    __tablename__ = "category"
    category_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    system_name = Column(String)
    friendly_name = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field) for field in CategoryDTO.model_fields
        }

    def to_model(self) -> CategoryDTO:
        return CategoryDTO(**self.to_dict())

    def to_dto(self) -> CategoryDTO:
        return self.to_model()


class AttributeAllowableValuesApplicableInEveryCategoryRecord(Base):
    __tablename__ = "attribute_allowable_values_applicable_in_every_category"
    attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    allowable_value = Column(String)

    def to_dict(self) -> dict:
        fields = (
            AttributeAllowableValuesApplicableInEveryCategoryDTO.model_fields
        )
        return {field: getattr(self, field) for field in fields}

    def to_model(self) -> AttributeAllowableValuesApplicableInEveryCategoryDTO:
        return AttributeAllowableValuesApplicableInEveryCategoryDTO(
            **self.to_dict()
        )

    def to_dto(self) -> AttributeAllowableValuesApplicableInEveryCategoryDTO:
        return self.to_model()


class AttributeAllowableValueInAnyCategoryRecord(Base):
    __tablename__ = "attribute_allowable_value_in_any_category"
    attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    value = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field)
            for field in AttributeAllowableValueInAnyCategoryDTO.model_fields
        }

    def to_model(self) -> AttributeAllowableValueInAnyCategoryDTO:
        return AttributeAllowableValueInAnyCategoryDTO(**self.to_dict())

    def to_dto(self) -> AttributeAllowableValueInAnyCategoryDTO:
        return self.to_model()


class AttributeRecord(Base):
    __tablename__ = "attribute"
    attribute_key = Column(PG_UUID(as_uuid=True), primary_key=True)
    system_name = Column(String)
    friendly_name = Column(String)
    attribute_type = Column(String)
    unit_measure_type = Column(String)

    def to_dict(self) -> dict:
        return {
            field: getattr(self, field) for field in AttributeDTO.model_fields
        }

    def to_model(self) -> AttributeDTO:
        return AttributeDTO(**self.to_dict())

    def to_dto(self) -> AttributeDTO:
        return self.to_model()
