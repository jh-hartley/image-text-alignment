CREATE OR REPLACE VIEW synthetic_product_view AS
SELECT
    p.product_key,
    p.system_name,
    p.friendly_name,
    dco.product_code,
    dco.product_title,
    dco.product_url,
    dco.category_0,
    dco.category_1,
    dco.category_2,
    dco.category_3,
    dco.description_text,
    dco.specification_text,
    dco.specification_attributes_xml,
    dco.image_url_1,
    dco.image_url_2,
    dco.image_url_3,
    dco.image_url_4,
    dco.image_url_5,
    dco.image_url_6,
    dco.image_url_7,
    dco.image_url_8,
    dco.image_url_9,
    dco.image_url_10,
    dco.now_price,
    dco.was_price,
    dco.save_message,
    dco.on_promotion,
    dco.review_count,
    dco.review_rating,
    pav.attribute_key,
    a.friendly_name AS attribute_name,
    pav.value,
    pav.unit,
    pav.minimum_value,
    pav.minimum_unit,
    pav.maximum_value,
    pav.maximum_unit,
    pav.range_qualifier_enum
FROM product p
LEFT JOIN dunelm_coalesce_output dco
    ON dco.product_url = p.system_name
LEFT JOIN product_attribute_value pav
    ON pav.product_key = p.product_key
LEFT JOIN attribute a
    ON a.attribute_key = pav.attribute_key; 