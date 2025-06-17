from sqlalchemy import Boolean, Column, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from src.common.db.base import Base


class DunelmCoalesceOutputRecord(Base):
    __tablename__ = "dunelm_coalesce_output"
    product_code = Column(String)
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
    on_promotion = Column(Boolean)
    video = Column(String)
    review_count = Column(String)
    review_rating = Column(Numeric)
    image_g = Column(String)
    roundel_g = Column(String)
    conscious_choice = Column(String)
    returns = Column(String)
    dunelm_dimensions_attributes_xml = Column(String)
    sample = Column(String)


class ImageFilePathMappingRecord(Base):
    __tablename__ = "image_file_path_mapping"
    image_path = Column(String)
    image_url = Column(String)
    product_url = Column(String)
    position = Column(String)


class RichTextSourceRecord(Base):
    __tablename__ = "rich_text_source"
    product_key = Column(UUID)
    rich_text = Column(String)
    rich_text_name = Column(String)
    rich_text_priority = Column(String)


class RecommendationRoundRecord(Base):
    __tablename__ = "recommendation_round"
    recommendation_round_key = Column(UUID)
    round_name = Column(String)
    timestamp = Column(String)


class RecommendationRecord(Base):
    __tablename__ = "recommendation"
    product_key = Column(UUID)
    attribute_key = Column(UUID)
    recommended_value = Column(String)
    unit = Column(String)
    minimum_value = Column(String)
    minimum_unit = Column(String)
    maximum_value = Column(String)
    maximum_unit = Column(String)
    original_expression = Column(String)
    range_qualifier_enum = Column(String)
    confidence_score = Column(String)
    recommendation_round_key = Column(UUID)
    is_disallowed = Column(String)


class ProductCategoryRecord(Base):
    __tablename__ = "product_category"
    product_key = Column(UUID)
    category_key = Column(UUID)


class ProductAttributeValueRecord(Base):
    __tablename__ = "product_attribute_value"
    product_key = Column(UUID)
    attribute_key = Column(UUID)
    value = Column(String)
    unit = Column(String)
    minimum_value = Column(String)
    minimum_unit = Column(String)
    maximum_value = Column(String)
    maximum_unit = Column(String)
    range_qualifier_enum = Column(String)


class ProductAttributeGapsRecord(Base):
    __tablename__ = "product_attribute_gaps"
    product_key = Column(UUID)
    attribute_key = Column(UUID)
    is_non_fillable = Column(String)
    non_fillable_reason = Column(String)


class ProductAttributeAllowableValueRecord(Base):
    __tablename__ = "product_attribute_allowable_value"
    product_key = Column(UUID)
    attribute_key = Column(UUID)
    value = Column(String)
    minimum_value = Column(String)
    minimum_unit = Column(String)
    maximum_value = Column(String)
    maximum_unit = Column(String)
    range_qualifier_enum = Column(String)


class ProductRecord(Base):
    __tablename__ = "product"
    product_key = Column(UUID)
    system_name = Column(String)
    friendly_name = Column(String)


class CategoryAttributeRecord(Base):
    __tablename__ = "category_attribute"
    category_attribute_key = Column(UUID)
    category_key = Column(UUID)
    attribute_key = Column(UUID)


class CategoryAllowableValueRecord(Base):
    __tablename__ = "category_allowable_value"
    category_attribute_key = Column(UUID)
    allowable_value = Column(String)
    allowable_unit_type = Column(String)
    minimum_value = Column(String)
    minimum_unit = Column(String)
    maximum_value = Column(String)
    maximum_unit = Column(String)
    range_qualifier_enum = Column(String)


class CategoryRecord(Base):
    __tablename__ = "category"
    category_key = Column(UUID)
    system_name = Column(String)
    friendly_name = Column(String)


class AttributeAllowableValuesApplicableInEveryCategoryRecord(Base):
    __tablename__ = "attribute_allowable_values_applicable_in_every_category"
    attribute_key = Column(UUID)
    allowable_value = Column(String)


class AttributeAllowableValueInAnyCategoryRecord(Base):
    __tablename__ = "attribute_allowable_value_in_any_category"
    attribute_key = Column(UUID)
    value = Column(String)


class AttributeRecord(Base):
    __tablename__ = "attribute"
    attribute_key = Column(UUID)
    system_name = Column(String)
    friendly_name = Column(String)
    attribute_type = Column(String)
    unit_measure_type = Column(String)
