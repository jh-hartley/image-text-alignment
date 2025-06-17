CREATE TABLE dunelm_coalesce_output (
    product_code TEXT,
    product_title TEXT,
    product_url TEXT,
    category_0 TEXT,
    category_1 TEXT,
    category_2 TEXT,
    category_3 TEXT,
    category_1_n TEXT,
    category_1_n_url TEXT,
    category_2_n TEXT,
    category_2_n_url TEXT,
    category_3_n TEXT,
    category_3_n_url TEXT,
    category_0_p TEXT,
    category_1_p TEXT,
    category_2_p TEXT,
    category_3_p TEXT,
    description_text TEXT,
    specification_text TEXT,
    specification_attributes_xml TEXT,
    image_url_1 TEXT,
    image_url_2 TEXT,
    image_url_3 TEXT,
    image_url_4 TEXT,
    image_url_5 TEXT,
    image_url_6 TEXT,
    image_url_7 TEXT,
    image_url_8 TEXT,
    image_url_9 TEXT,
    image_url_10 TEXT,
    description_bullet_points TEXT,
    now_price TEXT,
    was_price TEXT,
    save_message TEXT,
    on_promotion BOOLEAN,
    video TEXT,
    review_count TEXT,
    review_rating NUMERIC,
    image_g TEXT,
    roundel_g TEXT,
    conscious_choice TEXT,
    returns TEXT,
    dunelm_dimensions_attributes_xml TEXT,
    sample TEXT
); 

CREATE TABLE image_file_path_mapping (
    image_path TEXT,
    image_url TEXT,
    product_url TEXT,
    position TEXT
); 

CREATE TABLE rich_text_source (
    product_key UUID,
    rich_text TEXT,
    rich_text_name TEXT,
    rich_text_priority TEXT
);

CREATE TABLE recommendation_round (
    recommendation_round_key UUID,
    round_name TEXT,
    timestamp TEXT
);

CREATE TABLE recommendation (
    product_key UUID,
    attribute_key UUID,
    recommended_value TEXT,
    unit TEXT,
    minimum_value TEXT,
    minimum_unit TEXT,
    maximum_value TEXT,
    maximum_unit TEXT,
    original_expression TEXT,
    range_qualifier_enum TEXT,
    confidence_score TEXT,
    recommendation_round_key UUID,
    is_disallowed TEXT
);

CREATE TABLE product_category (
    product_key UUID,
    category_key UUID
);

CREATE TABLE product_attribute_value (
    product_key UUID,
    attribute_key UUID,
    value TEXT,
    unit TEXT,
    minimum_value TEXT,
    minimum_unit TEXT,
    maximum_value TEXT,
    maximum_unit TEXT,
    range_qualifier_enum TEXT
);

CREATE TABLE product_attribute_gaps (
    product_key UUID,
    attribute_key UUID,
    is_non_fillable TEXT,
    non_fillable_reason TEXT
);

CREATE TABLE product_attribute_allowable_value (
    product_key UUID,
    attribute_key UUID,
    value TEXT,
    minimum_value TEXT,
    minimum_unit TEXT,
    maximum_value TEXT,
    maximum_unit TEXT,
    range_qualifier_enum TEXT
);

CREATE TABLE product (
    product_key UUID,
    system_name TEXT,
    friendly_name TEXT
);

CREATE TABLE category_attribute (
    category_attribute_key UUID,
    category_key UUID,
    attribute_key UUID
);

CREATE TABLE category_allowable_value (
    category_attribute_key UUID,
    allowable_value TEXT,
    allowable_unit_type TEXT,
    minimum_value TEXT,
    minimum_unit TEXT,
    maximum_value TEXT,
    maximum_unit TEXT,
    range_qualifier_enum TEXT
);

CREATE TABLE category (
    category_key UUID,
    system_name TEXT,
    friendly_name TEXT
);

CREATE TABLE attribute_allowable_values_applicable_in_every_category (
    attribute_key UUID,
    allowable_value TEXT
);

CREATE TABLE attribute_allowable_value_in_any_category (
    attribute_key UUID,
    value TEXT
);

CREATE TABLE attribute (
    attribute_key UUID,
    system_name TEXT,
    friendly_name TEXT,
    attribute_type TEXT,
    unit_measure_type TEXT
); 