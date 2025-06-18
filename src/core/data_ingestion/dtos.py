from uuid import UUID

from pydantic import BaseModel


class DunelmCoalesceOutputDTO(BaseModel):
    product_code: str
    product_title: str
    product_url: str
    category_0: str | None
    category_1: str | None
    category_2: str | None
    category_3: str | None
    category_1_n: str | None
    category_1_n_url: str | None
    category_2_n: str | None
    category_2_n_url: str | None
    category_3_n: str | None
    category_3_n_url: str | None
    category_0_p: str | None
    category_1_p: str | None
    category_2_p: str | None
    category_3_p: str | None
    description_text: str | None
    specification_text: str | None
    specification_attributes_xml: str | None
    image_url_1: str | None
    image_url_2: str | None
    image_url_3: str | None
    image_url_4: str | None
    image_url_5: str | None
    image_url_6: str | None
    image_url_7: str | None
    image_url_8: str | None
    image_url_9: str | None
    image_url_10: str | None
    description_bullet_points: str | None
    now_price: str | None
    was_price: str | None
    save_message: str | None
    on_promotion: str | None
    video: str | None
    review_count: str | None
    review_rating: str | None
    image_g: str | None
    roundel_g: str | None
    conscious_choice: str | None
    returns: str | None
    dunelm_dimensions_attributes_xml: str | None
    sample: str | None


class ImageFilePathMappingDTO(BaseModel):
    image_path: str
    image_url: str
    product_url: str
    position: str | None


class RichTextSourceDTO(BaseModel):
    product_key: UUID
    rich_text: str
    rich_text_name: str
    rich_text_priority: str | None


class RecommendationRoundDTO(BaseModel):
    recommendation_round_key: UUID
    round_name: str
    timestamp: str


class RecommendationDTO(BaseModel):
    product_key: UUID
    attribute_key: UUID
    recommended_value: str
    unit: str | None
    minimum_value: str | None
    minimum_unit: str | None
    maximum_value: str | None
    maximum_unit: str | None
    original_expression: str | None
    range_qualifier_enum: str | None
    confidence_score: str | None
    recommendation_round_key: UUID
    is_disallowed: str | None


class ProductCategoryDTO(BaseModel):
    product_key: UUID
    category_key: UUID


class ProductAttributeValueDTO(BaseModel):
    product_key: UUID
    attribute_key: UUID
    value: str | None
    unit: str | None
    minimum_value: str | None
    minimum_unit: str | None
    maximum_value: str | None
    maximum_unit: str | None
    range_qualifier_enum: str | None


class ProductAttributeGapsDTO(BaseModel):
    product_key: UUID
    attribute_key: UUID
    is_non_fillable: str | None
    non_fillable_reason: str | None


class ProductAttributeAllowableValueDTO(BaseModel):
    product_key: UUID
    attribute_key: UUID
    value: str | None
    minimum_value: str | None
    minimum_unit: str | None
    maximum_value: str | None
    maximum_unit: str | None
    range_qualifier_enum: str | None


class ProductDTO(BaseModel):
    product_key: UUID
    system_name: str | None
    friendly_name: str | None


class CategoryAttributeDTO(BaseModel):
    category_attribute_key: UUID
    category_key: UUID
    attribute_key: UUID


class CategoryAllowableValueDTO(BaseModel):
    category_attribute_key: UUID
    allowable_value: str
    allowable_unit_type: str | None
    minimum_value: str | None
    minimum_unit: str | None
    maximum_value: str | None
    maximum_unit: str | None
    range_qualifier_enum: str | None


class CategoryDTO(BaseModel):
    category_key: UUID
    system_name: str | None
    friendly_name: str | None


class AttributeAllowableValuesApplicableInEveryCategoryDTO(BaseModel):
    attribute_key: UUID
    allowable_value: str


class AttributeAllowableValueInAnyCategoryDTO(BaseModel):
    attribute_key: UUID
    value: str


class AttributeDTO(BaseModel):
    attribute_key: UUID
    system_name: str
    friendly_name: str | None
    attribute_type: str | None
    unit_measure_type: str | None
